"""
百度百科文档加载器

这是一个专门为LangChain框架设计的百度百科内容加载器，用于从百度百科获取
权威的中文知识内容，特别适用于构建中文知识库和问答系统。

主要特性：
- 智能内容提取：优先提取摘要，回退到正文段落
- 容错机制：支持直接访问和搜索回退两种模式
- 内容限制：支持字符数限制，避免单次加载过多内容
- 依赖可选：BeautifulSoup为可选依赖，支持基础正则表达式模式

使用示例：
    # 基础用法
    loader = BaiduBaikeLoader("人工智能")
    documents = list(loader.lazy_load())
    
    # 高级用法
    loader = BaiduBaikeLoader(
        query="机器学习",
        load_max_docs=3,
        doc_content_chars_max=5000,
        timeout=15
    )
    for doc in loader.lazy_load():
        print(f"来源: {doc.metadata['source']}")
        print(f"内容: {doc.page_content[:200]}...")

依赖安装：
    pip install requests beautifulsoup4 langchain-core

作者：大模型技术团队
版本：1.0.0
"""

from __future__ import annotations

from typing import Iterator, List, Optional

import re
from urllib.parse import quote, urljoin, urlencode

import requests

# LangChain 0.3.x 版本导入
from langchain_core.document_loaders.base import BaseLoader
from langchain_core.documents import Document


class BaiduBaikeLoader(BaseLoader):
    """
    百度百科页面轻量级文档加载器
    
    这是一个专门用于从百度百科获取内容的文档加载器，适用于大模型的知识检索和问答系统。
    
    主要功能：
    - 智能解析查询词，优先尝试直接访问对应的百科条目页面
    - 如果直接访问失败，则回退到搜索页面并选择前N个相关条目链接
    - 自动提取条目的摘要和主要文本段落内容
    - 支持内容长度限制，避免单次加载过多文本
    
    使用场景：
    - 构建知识库时批量获取百科内容
    - 实时问答系统中获取权威信息
    - 研究助手工具中的信息收集

    参数说明
    ----------
    query : str
        要搜索的查询词或实体名称，例如："人工智能"、"Python编程"
    load_max_docs : int
        最大加载的条目页面数量，默认为2，建议不超过5以避免请求过多
    doc_content_chars_max : Optional[int]
        可选参数，如果设置则会将页面内容截断到指定字符数，用于控制单次加载的文本量
    timeout : int
        HTTP请求超时时间（秒），默认为12秒
    headers : Optional[dict]
        可选的额外HTTP请求头，默认提供桌面浏览器用户代理
    """

    def __init__(
        self,
        query: str,
        load_max_docs: int = 2,
        doc_content_chars_max: Optional[int] = None,
        timeout: int = 12,
        headers: Optional[dict] = None,
    ) -> None:
        """
        初始化百度百科加载器
        
        参数：
        - query: 搜索查询词，会自动去除首尾空格
        - load_max_docs: 最大文档数量，至少为1
        - doc_content_chars_max: 文档内容最大字符数限制
        - timeout: 请求超时时间
        - headers: 自定义HTTP请求头
        """
        self.query = query.strip()  # 去除查询词首尾空格
        self.load_max_docs = max(1, int(load_max_docs))  # 确保至少加载1个文档
        self.doc_content_chars_max = doc_content_chars_max
        self.timeout = timeout
        # 设置默认的浏览器请求头，模拟真实用户访问
        self.headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            ),
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",  # 优先中文，支持英文
        }
        # 如果用户提供了自定义请求头，则合并到默认请求头中
        if headers:
            self.headers.update(headers)

    def _get(self, url: str) -> requests.Response:
        """
        发送HTTP GET请求获取网页内容
        
        参数：
        - url: 目标网页URL
        
        返回：
        - requests.Response: HTTP响应对象
        
        异常：
        - 如果请求失败会抛出HTTPError异常
        """
        resp = requests.get(url, headers=self.headers, timeout=self.timeout, allow_redirects=True)
        resp.raise_for_status()  # 如果HTTP状态码不是2xx，则抛出异常
        return resp

    def _extract_text(self, html: str) -> str:
        """
        从HTML内容中提取纯文本
        
        这个方法会智能地从百度百科页面的HTML中提取主要内容，优先提取摘要部分，
        如果摘要不存在则提取正文段落。支持两种模式：
        1. 使用BeautifulSoup进行精确解析（推荐）
        2. 使用正则表达式进行简单清理（备用方案）
        
        参数：
        - html: 网页的HTML源码
        
        返回：
        - str: 提取的纯文本内容
        """
        try:
            from bs4 import BeautifulSoup  # 延迟导入，避免强制依赖
        except Exception:  # pragma: no cover
            # 备用方案：如果BeautifulSoup不可用，使用简单的正则表达式清理HTML
            text = re.sub(r"<script[\s\S]*?</script>|<style[\s\S]*?</style>", "", html)  # 移除脚本和样式
            text = re.sub(r"<[^>]+>", "\n", text)  # 将HTML标签替换为换行符
            text = re.sub(r"\n+", "\n", text)  # 合并多个换行符
            text = text.strip()
            # 如果设置了字符数限制，则截断文本
            if self.doc_content_chars_max is not None and self.doc_content_chars_max > 0:
                text = text[: self.doc_content_chars_max]
            return text

        soup = BeautifulSoup(html, "html.parser")

        # 优先提取摘要部分（百度百科的摘要通常包含最重要的信息）
        summary = soup.select_one(".lemma-summary, .lemmaWgt-lemmaSummary")
        parts: List[str] = []
        if summary:
            # 尝试提取摘要中的段落
            paras = summary.select(".para") or summary.find_all("div", class_="para")
            if paras:
                parts.extend(p.get_text(strip=True) for p in paras)
            else:
                parts.append(summary.get_text("\n", strip=True))

        # 如果摘要不存在，则提取正文段落
        if not parts:
            main = soup.select_one(".lemmaWgt-lemmaTitle, .lemmaWgt-lemmaInfo, .lemma-main")
            if not main:
                main = soup  # 如果找不到主要内容区域，则使用整个页面
            # 查找所有段落元素
            paras = main.find_all(["p", "div"], class_=re.compile(r"para|paragraph|content"))
            if paras:
                parts.extend(p.get_text(strip=True) for p in paras)
            else:
                # 最后的手段：提取所有文本，但排除导航和页脚
                for node in soup.select("#top,#bottom,script,style,nav,footer,header"):
                    node.extract()  # 移除不需要的元素
                text = soup.get_text("\n", strip=True)
                parts.append(text)

        # 合并所有文本段落，过滤空内容
        text = "\n".join([p for p in parts if p])
        # 如果设置了字符数限制，则截断文本
        if self.doc_content_chars_max is not None and self.doc_content_chars_max > 0:
            text = text[: self.doc_content_chars_max]
        return text

    def _search_links(self, html: str) -> List[str]:
        """
        从百度百科搜索页面中提取候选条目链接
        
        当直接访问条目页面失败时，会回退到搜索页面，然后从这个方法中提取
        相关的条目链接。支持两种解析模式：
        1. 使用BeautifulSoup精确解析（推荐）
        2. 使用正则表达式近似匹配（备用方案）
        
        参数：
        - html: 搜索页面的HTML源码
        
        返回：
        - List[str]: 候选条目链接列表，最多返回load_max_docs个链接
        """
        try:
            from bs4 import BeautifulSoup  # 延迟导入
        except Exception:  # pragma: no cover
            # 备用方案：使用正则表达式近似匹配百度百科条目链接
            hrefs = re.findall(r"href=\"(/item/[^\"]+)\"", html)
            seen: List[str] = []  # 用于去重的已访问链接集合
            out: List[str] = []   # 输出链接列表
            for h in hrefs:
                u = urljoin("https://baike.baidu.com/", h)  # 构建完整URL
                if u not in seen:
                    seen.append(u)
                    out.append(u)
                if len(out) >= self.load_max_docs:  # 达到最大文档数限制时停止
                    break
            return out

        soup = BeautifulSoup(html, "html.parser")
        links: List[str] = []
        # 查找典型的搜索结果链接（百度百科搜索页面的链接选择器）
        for a in soup.select("a.result-title, .search-list a[href^='/item/'], a[href^='/item/']"):
            href = a.get("href")
            if not href:
                continue
            url = urljoin("https://baike.baidu.com/", href)  # 构建完整URL
            if url not in links:  # 避免重复链接
                links.append(url)
            if len(links) >= self.load_max_docs:  # 达到最大文档数限制时停止
                break
        return links

    def lazy_load(self) -> Iterator[Document]:
        """
        懒加载方式获取百度百科文档
        
        这是LangChain文档加载器的核心方法，采用懒加载模式，即只有在需要时才
        实际获取文档内容。加载策略分为两个阶段：
        
        阶段1：尝试直接访问条目页面
        - 构建直接的条目URL（如：https://baike.baidu.com/item/人工智能）
        - 如果成功且返回的是条目页面，直接提取内容
        - 如果重定向到搜索页面，保存HTML用于后续解析
        
        阶段2：解析搜索页面获取相关链接
        - 如果直接访问失败，使用搜索接口
        - 从搜索结果中提取前N个相关条目链接
        - 逐个访问这些链接并提取内容
        
        返回：
        - Iterator[Document]: 文档迭代器，每个Document包含页面内容和元数据
        """
        if not self.query:
            return iter(())  # 如果查询为空，返回空迭代器

        # 阶段1：尝试直接访问条目URL（最理想的情况）
        direct_url = f"https://baike.baidu.com/item/{quote(self.query)}"
        try:
            resp = self._get(direct_url)
            final_url = resp.url
            # 检查是否成功访问到条目页面（URL中包含/item/）
            if "/item/" in final_url:
                text = self._extract_text(resp.text)
                if text.strip():  # 确保提取到了有效内容
                    yield Document(
                        page_content=text, 
                        metadata={"source": final_url, "source_type": "baike"}
                    )
                    # 如果只需要一个文档，直接返回
                    if self.load_max_docs <= 1:
                        return
            # 如果重定向到搜索页面，保存HTML用于后续解析
            html = resp.text
        except Exception:
            # 直接访问失败，回退到显式搜索接口
            params = urlencode({"word": self.query})
            search_url = f"https://baike.baidu.com/search?{params}"
            try:
                resp = self._get(search_url)
                html = resp.text
            except Exception:
                return iter(())  # 搜索也失败，返回空迭代器

        # 阶段2：解析搜索页面获取相关条目链接
        try:
            links = self._search_links(html)
        except Exception:
            links = []  # 解析失败，使用空链接列表

        # 逐个访问找到的链接并提取内容
        for url in links[: self.load_max_docs]:
            try:
                resp = self._get(url)
                text = self._extract_text(resp.text)
                if text.strip():  # 确保提取到了有效内容
                    yield Document(
                        page_content=text, 
                        metadata={"source": resp.url, "source_type": "baike"}
                    )
            except Exception:
                continue  # 单个链接失败不影响其他链接的处理
