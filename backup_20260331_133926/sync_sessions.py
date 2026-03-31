#!/usr/bin/env python3
"""
会话同步脚本
自动同步浏览器会话和微信会话的信息
"""

import json
import os
from datetime import datetime
from pathlib import Path

class SessionSync:
    def __init__(self):
        self.workspace = Path("/Users/carson/.openclaw/workspace")
        self.shared_memory = self.workspace / "shared_memory.md"
        self.session_log = self.workspace / "session_log.json"
        
    def log_session_activity(self, session_type, activity, details):
        """记录会话活动"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "session_type": session_type,  # "browser" 或 "weixin"
            "activity": activity,
            "details": details
        }
        
        # 读取现有日志
        if self.session_log.exists():
            with open(self.session_log, 'r', encoding='utf-8') as f:
                logs = json.load(f)
        else:
            logs = {"sessions": []}
        
        # 添加新日志
        logs["sessions"].append(log_entry)
        
        # 只保留最近100条
        if len(logs["sessions"]) > 100:
            logs["sessions"] = logs["sessions"][-100:]
        
        # 保存日志
        with open(self.session_log, 'w', encoding='utf-8') as f:
            json.dump(logs, f, indent=2, ensure_ascii=False)
        
        print(f"📝 记录会话活动: {session_type} - {activity}")
        
    def update_project_status(self, project_name, updates):
        """更新项目状态"""
        status_file = self.workspace / "project_status.json"
        
        if status_file.exists():
            with open(status_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = {"projects": {}}
        
        # 更新项目信息
        if project_name not in data["projects"]:
            data["projects"][project_name] = {
                "name": project_name,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "progress": 0,
                "tasks": []
            }
        
        project = data["projects"][project_name]
        project["last_updated"] = datetime.now().isoformat()
        
        # 应用更新
        for key, value in updates.items():
            if key == "progress":
                project["progress"] = value
            elif key == "status":
                project["status"] = value
            elif key == "task_completed":
                # 标记任务完成
                for task in project.get("tasks", []):
                    if task["name"] == value:
                        task["status"] = "completed"
                        task["completed_at"] = datetime.now().isoformat()
            elif key == "new_task":
                # 添加新任务
                if "tasks" not in project:
                    project["tasks"] = []
                project["tasks"].append({
                    "name": value,
                    "status": "pending",
                    "created_at": datetime.now().isoformat()
                })
        
        # 保存更新
        with open(status_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"📊 更新项目状态: {project_name}")
        
    def get_session_summary(self, session_type=None, limit=10):
        """获取会话摘要"""
        if not self.session_log.exists():
            return "暂无会话记录"
        
        with open(self.session_log, 'r', encoding='utf-8') as f:
            logs = json.load(f)
        
        sessions = logs.get("sessions", [])
        
        if session_type:
            sessions = [s for s in sessions if s["session_type"] == session_type]
        
        sessions = sessions[-limit:]  # 获取最近记录
        
        summary = f"📋 会话摘要 (最近{len(sessions)}条)\n"
        summary += "=" * 40 + "\n"
        
        for session in sessions:
            time = datetime.fromisoformat(session["timestamp"]).strftime("%H:%M")
            summary += f"[{time}] {session['session_type']}: {session['activity']}\n"
        
        return summary
    
    def get_active_projects(self):
        """获取活跃项目"""
        status_file = self.workspace / "project_status.json"
        
        if not status_file.exists():
            return "暂无项目数据"
        
        with open(status_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        projects = data.get("projects", {})
        
        summary = "🚀 活跃项目\n"
        summary += "=" * 40 + "\n"
        
        for name, project in projects.items():
            progress = project.get("progress", 0)
            status = project.get("status", "unknown")
            last_updated = project.get("last_updated", "")
            
            if last_updated:
                try:
                    last_time = datetime.fromisoformat(last_updated).strftime("%m-%d %H:%M")
                except:
                    last_time = last_updated
            else:
                last_time = "未知"
            
            summary += f"📁 {name}\n"
            summary += f"   进度: {progress}% | 状态: {status}\n"
            summary += f"   最后更新: {last_time}\n"
            
            # 显示最近任务
            tasks = project.get("tasks", [])
            if tasks:
                recent_tasks = tasks[-3:]  # 最近3个任务
                for task in recent_tasks:
                    task_status = task.get("status", "pending")
                    status_icon = "✅" if task_status == "completed" else "⏳"
                    summary += f"   {status_icon} {task['name']}\n"
            
            summary += "\n"
        
        return summary
    
    def sync_from_browser(self, message):
        """从浏览器会话同步信息"""
        print("🔄 从浏览器会话同步...")
        
        # 记录浏览器会话活动
        self.log_session_activity("browser", "消息同步", message)
        
        # 更新共享记忆
        self.update_shared_memory("browser", message)
        
        print("✅ 浏览器会话同步完成")
        
    def sync_from_weixin(self, message):
        """从微信会话同步信息"""
        print("🔄 从微信会话同步...")
        
        # 记录微信会话活动
        self.log_session_activity("weixin", "消息同步", message)
        
        # 更新共享记忆
        self.update_shared_memory("weixin", message)
        
        print("✅ 微信会话同步完成")
        
    def update_shared_memory(self, source, content):
        """更新共享记忆文件"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        update_entry = f"""
## 💬 {timestamp} - {source.upper()}会话
{content}

---
"""
        
        # 读取现有内容
        if self.shared_memory.exists():
            with open(self.shared_memory, 'r', encoding='utf-8') as f:
                existing = f.read()
        else:
            existing = "# 🧠 共享记忆文件\n\n"
        
        # 在文件开头添加新内容
        lines = existing.split('\n')
        if len(lines) > 50:  # 如果文件太长，截断
            lines = lines[:50]
        
        new_content = update_entry + '\n'.join(lines)
        
        # 写入文件
        with open(self.shared_memory, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"📝 更新共享记忆: {source}")

def main():
    """主函数 - 测试同步功能"""
    sync = SessionSync()
    
    print("🔄 会话同步系统测试")
    print("=" * 50)
    
    # 测试日志记录
    sync.log_session_activity("weixin", "测试同步", "微信会话测试消息")
    sync.log_session_activity("browser", "测试同步", "浏览器会话测试消息")
    
    # 测试项目更新
    sync.update_project_status("website", {
        "progress": 45,
        "status": "in_progress",
        "task_completed": "首页设计"
    })
    
    # 显示摘要
    print("\n" + "=" * 50)
    print(sync.get_session_summary())
    
    print("\n" + "=" * 50)
    print(sync.get_active_projects())
    
    print("\n✅ 同步系统测试完成")

if __name__ == "__main__":
    main()