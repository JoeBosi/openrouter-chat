#!/usr/bin/env python3
"""
Debug script to check system prompt generation
"""

import os
import sys
import tkinter as tk

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def debug_prompt():
    """Debug system prompt generation"""
    try:
        from chat_gui import OpenRouterChatGUI
        
        # Create test window
        root = tk.Tk()
        root.withdraw()
        
        # Create GUI instance
        chat = OpenRouterChatGUI(root)
        
        print("🔍 Debug System Prompt Generation")
        print("=" * 50)
        
        # Show default instructions
        print("Default instructions:")
        for key, value in chat.additional_instructions.items():
            print(f"  {key}: {value}")
        
        print("\nGenerated system prompt:")
        prompt = chat.build_system_prompt()
        print(f"'{prompt}'")
        
        print(f"\nPrompt length: {len(prompt)}")
        
        # Test with custom instructions
        print("\n" + "=" * 50)
        print("Testing with custom instructions:")
        
        chat.additional_instructions['length'] = 'short'
        chat.additional_instructions['tone'] = 'casual'
        chat.additional_instructions['style'] = 'technical'
        chat.additional_instructions['format'] = 'bullet_points'
        chat.additional_instructions['custom'] = 'Be very helpful'
        
        print("Custom instructions:")
        for key, value in chat.additional_instructions.items():
            print(f"  {key}: {value}")
        
        print("\nGenerated system prompt:")
        prompt = chat.build_system_prompt()
        print(f"'{prompt}'")
        
        print(f"\nPrompt length: {len(prompt)}")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")

if __name__ == "__main__":
    debug_prompt()
