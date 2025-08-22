#!/usr/bin/env python3
"""
Test script to demonstrate all questions the Healthcare QA system can answer
"""

import requests
import json

def test_medical_questions():
    """Test various medical questions to demonstrate system capabilities"""
    
    questions = [
        # Aspirin Questions
        "What are the side effects of aspirin?",
        "What are aspirin side effects?",
        "What are the adverse effects of aspirin?",
        "What reactions can aspirin cause?",
        
        # Diabetes Questions  
        "What are the symptoms of diabetes?",
        "What are diabetes symptoms?",
        "What are the signs of diabetes?",
        "How is diabetes treated?",
        "How is diabetes managed?",
        "What is diabetes?",
        "What are the types of diabetes?",
        "What are diabetes complications?",
        
        # Hypertension Questions
        "What are the risk factors for hypertension?",
        "What causes hypertension?",
        "What are hypertension risk factors?",
        "How is hypertension treated?",
        "How is high blood pressure treated?",
        "What is hypertension?",
        "What is high blood pressure?",
        "What medications treat hypertension?",
        
        # Pneumonia Questions
        "What are the symptoms of pneumonia?",
        "What are pneumonia symptoms?",
        "What are the signs of pneumonia?",
        "What causes pneumonia?",
        "How is pneumonia diagnosed?",
        "How is pneumonia treated?",
        "What is pneumonia?",
        
        # Insulin Questions
        "What are the types of insulin?",
        "What types of insulin are there?",
        "How is insulin administered?",
        "What are insulin side effects?",
        "What is insulin?",
        
        # General Questions
        "What medications are used for diabetes?",
        "What is a heart attack?",
        "What are heart attack symptoms?",
    ]
    
    print("=" * 80)
    print("HEALTHCARE BERT QA SYSTEM - COMPREHENSIVE QUESTION TEST")
    print("=" * 80)
    print()
    
    successful_answers = 0
    high_confidence_answers = 0
    
    for i, question in enumerate(questions, 1):
        try:
            response = requests.post(
                'http://localhost:5000/api/v1/ask', 
                json={'question': question}, 
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                answer = data['answer']
                confidence = data['confidence']
                category = data.get('category', 'general')
                
                print(f"{i:2d}. QUESTION: {question}")
                print(f"    ANSWER: {answer[:100]}{'...' if len(answer) > 100 else ''}")
                print(f"    CONFIDENCE: {confidence:.1%}")
                print(f"    CATEGORY: {category}")
                print()
                
                successful_answers += 1
                if confidence >= 0.9:
                    high_confidence_answers += 1
                    
            else:
                print(f"{i:2d}. QUESTION: {question}")
                print(f"    ERROR: HTTP {response.status_code}")
                print()
                
        except Exception as e:
            print(f"{i:2d}. QUESTION: {question}")
            print(f"    ERROR: {e}")
            print()
    
    print("=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"Total Questions Tested: {len(questions)}")
    print(f"Successful Answers: {successful_answers}")
    print(f"High Confidence Answers (≥90%): {high_confidence_answers}")
    print(f"Success Rate: {successful_answers/len(questions):.1%}")
    print(f"High Confidence Rate: {high_confidence_answers/len(questions):.1%}")

if __name__ == "__main__":
    test_medical_questions()
