#!/usr/bin/env python3
"""
Debug instruction combinations
"""

import os
import sys
import tkinter as tk

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_combinations():
    """Debug instruction combinations"""
    try:
        from chat_gui import OpenRouterChatGUI
        
        # Create test window
        root = tk.Tk()
        root.withdraw()
        
        # Create GUI instance
        chat = OpenRouterChatGUI(root)
        
        print("🔍 Debug Instruction Combinations")
        print("=" * 50)
        
        # Test case 1
        print("Test Case 1:")
        case1 = {
            'length': 'short',
            'tone': 'formal',
            'style': 'technical',
            'format': 'bullet_points',
            'custom': 'Include examples'
        }
        
        chat.additional_instructions.update(case1)
        prompt1 = chat.build_system_prompt()
        print(f"Prompt: '{prompt1}'")
        
        print(f"Contains 'concise' or 'brief': {'concise' in prompt1.lower() or 'brief' in prompt1.lower()}")
        print(f"Contains 'formal' or 'respectful': {'formal' in prompt1.lower() or 'respectful' in prompt1.lower()}")
        print(f"Contains 'technical' or 'precise': {'technical' in prompt1.lower() or 'precise' in prompt1.lower()}")
        print(f"Contains 'bullet': {'bullet' in prompt1.lower()}")
        print(f"Contains 'examples': {'examples' in prompt1.lower()}")
        
        print("\n" + "=" * 50)
        
        # Test case 2
        print("Test Case 2:")
        case2 = {
            'length': 'long',
            'tone': 'friendly',
            'style': 'creative',
            'format': 'numbered_list',
            'custom': 'Use metaphors'
        }
        
        chat.additional_instructions.update(case2)
        prompt2 = chat.build_system_prompt()
        print(f"Prompt: '{prompt2}'")
        
        print(f"Contains 'comprehensive' or 'detailed': {'comprehensive' in prompt2.lower() or 'detailed' in prompt2.lower()}")
        print(f"Contains 'warm' or 'approachable': {'warm' in prompt2.lower() or 'approachable' in prompt2.lower()}")
        print(f"Contains 'creative' or 'engaging': {'creative' in prompt2.lower() or 'engaging' in prompt2.lower()}")
        print(f"Contains 'numbered': {'numbered' in prompt2.lower()}")
        print(f"Contains 'metaphors': {'metaphors' in prompt2.lower()}")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")

if __name__ == "__main__":
    debug_combinations()
