/**
 * 此脚本用于生成空的模板数据库文件（template.sqlite）
 * 该文件将在应用打包时被包含，并在用户首次启动应用时作为初始数据库
 */

const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const templatePath = path.join(__dirname, 'template.sqlite');
const sqlitePath = path.join(__dirname, 'empty.db.sqlite');

// 如果存在旧的模板文件，先删除
if (fs.existsSync(templatePath)) {
  console.log('删除旧的模板数据库...');
  fs.unlinkSync(templatePath);
}

// 如果存在临时数据库文件，先删除
if (fs.existsSync(sqlitePath)) {
  console.log('删除临时数据库文件...');
  fs.unlinkSync(sqlitePath);
}

try {
  console.log('设置临时数据库路径...');
  // 设置 DATABASE_URL 环境变量
  process.env.DATABASE_URL = `file:${sqlitePath}`;

  console.log('执行 prisma db push 创建新的数据库架构...');
  // 执行 prisma db push 创建数据库架构
  execSync('npx prisma db push', { stdio: 'inherit' });

  console.log('将生成的数据库文件复制为模板...');
  // 复制生成的数据库文件为模板
  fs.copyFileSync(sqlitePath, templatePath);

  console.log(`✅ 模板数据库已成功生成: ${templatePath}`);
} catch (error) {
  console.error('❌ 生成模板数据库失败:', error);
  process.exit(1);
} finally {
  // 清理: 删除临时数据库文件
  if (fs.existsSync(sqlitePath)) {
    console.log('清理临时数据库文件...');
    fs.unlinkSync(sqlitePath);
  }
}
