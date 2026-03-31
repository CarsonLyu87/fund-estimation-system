#!/usr/bin/env python3
"""
任务管理系统
跟踪浏览器和微信会话中的所有任务
"""

import json
import os
from datetime import datetime
from pathlib import Path

class TaskManager:
    def __init__(self):
        self.workspace = Path("/Users/carson/.openclaw/workspace")
        self.tasks_file = self.workspace / "tasks.json"
        self.init_tasks_file()
    
    def init_tasks_file(self):
        """初始化任务文件"""
        if not self.tasks_file.exists():
            default_tasks = {
                "version": "1.0",
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "tasks": [],
                "projects": {},
                "session_tasks": {
                    "browser": [],
                    "weixin": []
                }
            }
            self.save_tasks(default_tasks)
    
    def load_tasks(self):
        """加载任务数据"""
        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            self.init_tasks_file()
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                return json.load(f)
    
    def save_tasks(self, data):
        """保存任务数据"""
        data["last_updated"] = datetime.now().isoformat()
        with open(self.tasks_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    def create_task(self, title, description="", session="unknown", project=None, priority="medium"):
        """创建新任务"""
        data = self.load_tasks()
        
        task_id = f"task_{len(data['tasks']) + 1:03d}"
        
        task = {
            "id": task_id,
            "title": title,
            "description": description,
            "session": session,  # browser, weixin, etc.
            "project": project,
            "priority": priority,  # low, medium, high, urgent
            "status": "pending",  # pending, in_progress, completed, blocked
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "completed_at": None,
            "assigned_to": session,
            "notes": []
        }
        
        data["tasks"].append(task)
        
        # 添加到会话任务列表
        if session not in data["session_tasks"]:
            data["session_tasks"][session] = []
        data["session_tasks"][session].append(task_id)
        
        # 添加到项目（如果有）
        if project and project in data["projects"]:
            if "task_ids" not in data["projects"][project]:
                data["projects"][project]["task_ids"] = []
            data["projects"][project]["task_ids"].append(task_id)
        
        self.save_tasks(data)
        
        print(f"✅ 创建任务: {task_id} - {title}")
        return task_id
    
    def update_task_status(self, task_id, status, notes=""):
        """更新任务状态"""
        data = self.load_tasks()
        
        for task in data["tasks"]:
            if task["id"] == task_id:
                old_status = task["status"]
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                
                if status == "completed":
                    task["completed_at"] = datetime.now().isoformat()
                
                if notes:
                    note_entry = {
                        "timestamp": datetime.now().isoformat(),
                        "status_change": f"{old_status} → {status}",
                        "notes": notes
                    }
                    task["notes"].append(note_entry)
                
                print(f"📊 更新任务状态: {task_id} - {old_status} → {status}")
                break
        
        self.save_tasks(data)
    
    def add_task_note(self, task_id, note):
        """添加任务备注"""
        data = self.load_tasks()
        
        for task in data["tasks"]:
            if task["id"] == task_id:
                note_entry = {
                    "timestamp": datetime.now().isoformat(),
                    "notes": note
                }
                task["notes"].append(note_entry)
                task["updated_at"] = datetime.now().isoformat()
                
                print(f"📝 添加任务备注: {task_id}")
                break
        
        self.save_tasks(data)
    
    def get_task(self, task_id):
        """获取任务详情"""
        data = self.load_tasks()
        
        for task in data["tasks"]:
            if task["id"] == task_id:
                return task
        
        return None
    
    def list_tasks(self, filters=None):
        """列出任务"""
        data = self.load_tasks()
        
        if filters is None:
            filters = {}
        
        filtered_tasks = data["tasks"]
        
        # 应用过滤器
        if "session" in filters:
            filtered_tasks = [t for t in filtered_tasks if t["session"] == filters["session"]]
        
        if "status" in filters:
            filtered_tasks = [t for t in filtered_tasks if t["status"] == filters["status"]]
        
        if "project" in filters:
            filtered_tasks = [t for t in filtered_tasks if t.get("project") == filters["project"]]
        
        if "priority" in filters:
            filtered_tasks = [t for t in filtered_tasks if t["priority"] == filters["priority"]]
        
        return filtered_tasks
    
    def get_session_summary(self, session):
        """获取会话任务摘要"""
        tasks = self.list_tasks({"session": session})
        
        summary = {
            "total": len(tasks),
            "pending": sum(1 for t in tasks if t["status"] == "pending"),
            "in_progress": sum(1 for t in tasks if t["status"] == "in_progress"),
            "completed": sum(1 for t in tasks if t["status"] == "completed"),
            "blocked": sum(1 for t in tasks if t["status"] == "blocked")
        }
        
        return summary
    
    def create_project(self, name, description=""):
        """创建项目"""
        data = self.load_tasks()
        
        if name not in data["projects"]:
            data["projects"][name] = {
                "name": name,
                "description": description,
                "created_at": datetime.now().isoformat(),
                "last_updated": datetime.now().isoformat(),
                "status": "active",
                "task_ids": []
            }
            
            self.save_tasks(data)
            print(f"🏗️ 创建项目: {name}")
            return True
        
        return False
    
    def get_browser_tasks_summary(self):
        """获取浏览器任务摘要"""
        return self.get_session_summary("browser")
    
    def check_browser_tasks_completion(self):
        """检查浏览器任务完成情况"""
        browser_tasks = self.list_tasks({"session": "browser"})
        
        if not browser_tasks:
            return {
                "has_tasks": False,
                "message": "没有找到浏览器任务记录",
                "tasks": []
            }
        
        completed = [t for t in browser_tasks if t["status"] == "completed"]
        pending = [t for t in browser_tasks if t["status"] in ["pending", "in_progress"]]
        
        return {
            "has_tasks": True,
            "total": len(browser_tasks),
            "completed": len(completed),
            "pending": len(pending),
            "completion_rate": len(completed) / len(browser_tasks) * 100 if browser_tasks else 0,
            "completed_tasks": [t["title"] for t in completed],
            "pending_tasks": [t["title"] for t in pending]
        }

def main():
    """测试任务管理系统"""
    print("🧠 任务管理系统测试")
    print("=" * 50)
    
    manager = TaskManager()
    
    # 创建一些测试任务
    task1 = manager.create_task(
        "测试浏览器任务",
        "这是一个测试任务",
        session="browser",
        project="website",
        priority="medium"
    )
    
    task2 = manager.create_task(
        "测试微信任务", 
        "另一个测试任务",
        session="weixin",
        project="fund_monitor",
        priority="high"
    )
    
    # 更新任务状态
    manager.update_task_status(task1, "completed", "测试完成")
    manager.update_task_status(task2, "in_progress", "开始处理")
    
    # 获取摘要
    print("\n📊 浏览器任务摘要:")
    browser_summary = manager.get_browser_tasks_summary()
    print(f"  总计: {browser_summary['total']}")
    print(f"  待办: {browser_summary['pending']}")
    print(f"  进行中: {browser_summary['in_progress']}")
    print(f"  已完成: {browser_summary['completed']}")
    
    print("\n📊 检查浏览器任务完成情况:")
    completion = manager.check_browser_tasks_completion()
    if completion["has_tasks"]:
        print(f"  完成率: {completion['completion_rate']:.1f}%")
        print(f"  已完成: {', '.join(completion['completed_tasks'])}")
        print(f"  待完成: {', '.join(completion['pending_tasks'])}")
    else:
        print("  无任务记录")
    
    print("\n✅ 任务管理系统测试完成")

if __name__ == "__main__":
    main()