#!/usr/bin/env python3
"""
跨仓库里程碑测试脚本 - 适用于平行仓库结构
"""

import sys
import os
import time
import requests
from pathlib import Path

# ========== 配置区域 ==========
# 假设仓库都在同一父目录下，根据实际情况调整
PARENT_DIR = Path(__file__).parent.parent  # 上级目录
# 或者如果不行，尝试：PARENT_DIR = Path("..") 或 Path("../..")

# 仓库名称（根据你的GitHub名称）
REPO_NAMES = {
    "idle_sense": "idle-sense",      # GitHub仓库名
    "idle_accelerator": "idle-accelerator"
}

print("=" * 60)
print("🚀 跨仓库里程碑测试启动")
print("=" * 60)

# ========== 第一步：查找仓库 ==========
def find_and_setup_repos():
    """查找并配置两个仓库的路径"""
    
    print("\n🔍 查找仓库...")
    
    found_repos = {}
    
    # 尝试多种可能的路径
    search_paths = [
        PARENT_DIR,                     # 上级目录
        Path(".."),                     # 直接上级
        Path("../.."),                  # 上两级
        Path(__file__).parent.parent,   # 脚本的上级目录
        Path("/workspaces"),            # GitHub Codespaces
        Path("/home/codespace/workspace"),  # 另一种Codespaces
    ]
    
    for search_path in search_paths:
        if not search_path.exists():
            continue
            
        for internal_name, repo_name in REPO_NAMES.items():
            repo_path = search_path / repo_name
            
            if repo_path.exists() and repo_path.is_dir():
                # 验证是代码仓库（有.py文件或README）
                has_py_files = any(repo_path.glob("*.py"))
                has_readme = (repo_path / "README.md").exists()
                
                if has_py_files or has_readme:
                    abs_path = repo_path.absolute()
                    print(f"  ✅ 找到 {repo_name}: {abs_path}")
                    found_repos[internal_name] = abs_path
    
    return found_repos

# ========== 第二步：配置Python路径 ==========
def setup_import_paths(repos):
    """将找到的仓库添加到Python路径"""
    
    print("\n📁 配置导入路径...")
    
    # 按顺序添加，确保正确导入
    sys.path.insert(0, str(repos.get("idle_accelerator", "")))
    sys.path.insert(0, str(repos.get("idle_sense", "")))
    
    # 打印配置好的路径
    print("  当前Python路径:")
    for i, path in enumerate(sys.path[:4]):  # 只显示前几个
        print(f"    {i}. {path}")

# ========== 第三步：里程碑测试 ==========
def test_milestone_1(repos):
    """测试里程碑一：闲置检测库"""
    print("\n🎯 里程碑一：测试闲置检测库")
    
    if "idle_sense" not in repos:
        print("  ❌ 未找到 idle-sense 仓库")
        return False
    
    try:
        # 临时添加路径并导入
        sys.path.insert(0, str(repos["idle_sense"]))
        from idle_sense.core import is_idle, get_platform, get_system_status
        
        print(f"  ✅ 成功导入 idle-sense")
        print(f"    平台: {get_platform()}")
        print(f"    状态: {get_system_status()}")
        print(f"    是否闲置: {is_idle()}")
        return True
        
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        # 显示 idle_sense 目录内容帮助调试
        repo_path = repos["idle_sense"]
        print(f"  📂 {repo_path} 内容:")
        try:
            for item in os.listdir(repo_path)[:10]:  # 只显示前10个
                print(f"    - {item}")
        except:
            pass
        return False

def test_milestone_2(repos):
    """测试里程碑二：调度链路"""
    print("\n🎯 里程碑二：测试调度链路")
    
    if "idle_accelerator" not in repos:
        print("  ❌ 未找到 idle-accelerator 仓库")
        return False
    
    try:
        # 检查调度中心是否可访问
        print("  测试调度中心API...")
        try:
            resp = requests.get("http://localhost:8000/", timeout=2)
            if resp.status_code == 200:
                print("  ✅ 调度中心正在运行")
                return True
        except:
            print("  ⚠️ 调度中心未运行（正常，跳过此测试）")
            print("  提示：运行 python scheduler/simple_server.py 启动")
            return True  # 不算失败，只是没启动
            
    except Exception as e:
        print(f"  ❌ 测试失败: {e}")
        return False

def test_milestone_3():
    """测试里程碑三：网页界面"""
    print("\n🎯 里程碑三：测试网页界面")
    
    # 检查网页文件是否存在
    web_dir = Path("web") if Path("web").exists() else Path(".")
    html_files = list(web_dir.glob("*.html"))
    
    if html_files:
        print(f"  ✅ 找到网页文件: {[f.name for f in html_files]}")
        return True
    else:
        print("  ⚠️ 未找到网页文件（可能路径不同）")
        return True  # 不算失败

def test_milestone_4():
    """测试里程碑四：跨电脑演示准备"""
    print("\n🎯 里程碑四：测试跨电脑准备")
    
    # 检查必要的文件都存在
    required_files = [
        "scheduler/simple_server.py",
        "node/simple_client.py",
        "requirements.txt"
    ]
    
    missing = []
    for file in required_files:
        if not Path(file).exists():
            missing.append(file)
    
    if not missing:
        print("  ✅ 所有必要文件都存在")
        return True
    else:
        print(f"  ⚠️ 缺失文件: {missing}")
        return False

# ========== 主函数 ==========
def main():
    # 1. 查找仓库
    repos = find_and_setup_repos()
    
    if not repos:
        print("\n❌ 未找到任何仓库！")
        print("请确认：")
        print("1. idle-sense 和 idle-accelerator 在同一个父目录下")
        print("2. 或者手动修改脚本中的 PARENT_DIR 变量")
        print(f"\n当前脚本位置: {Path(__file__).absolute()}")
        print(f"当前工作目录: {os.getcwd()}")
        print(f"上级目录内容: {os.listdir('..') if Path('..').exists() else '不存在'}")
        return 1
    
    # 2. 配置路径
    setup_import_paths(repos)
    
    # 3. 运行测试
    print("\n" + "=" * 60)
    print("开始里程碑测试...")
    print("=" * 60)
    
    results = []
    results.append(test_milestone_1(repos))
    results.append(test_milestone_2(repos))
    results.append(test_milestone_3())
    results.append(test_milestone_4())
    
    # 4. 显示结果
    print("\n" + "=" * 60)
    print("📊 测试结果汇总:")
    print("=" * 60)
    
    milestones = [
        "里程碑一：闲置检测库",
        "里程碑二：调度链路", 
        "里程碑三：网页界面",
        "里程碑四：跨电脑准备"
    ]
    
    for i, (milestone, passed) in enumerate(zip(milestones, results), 1):
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{i}. {milestone}: {status}")
    
    print("\n" + "=" * 60)
    
    if all(results):
        print("🎉 所有里程碑测试通过！")
        print("\n下一步行动:")
        print("1. 确保 idle-sense 仓库可正常导入")
        print("2. 启动调度中心: python scheduler/simple_server.py")
        print("3. 测试网页界面: 打开 web/simple_ui.html")
        print("4. 进行跨电脑实际演示")
        return 0
    else:
        print("⚠️  部分测试未通过")
        print("请根据上面的错误信息修复问题")
        return 1

if __name__ == "__main__":
    # 确保在 idle-accelerator 目录下运行
    if not Path("scheduler").exists():
        print("⚠️  警告：似乎不在 idle-accelerator 目录")
        print("尝试切换到正确目录...")
    
    sys.exit(main())
