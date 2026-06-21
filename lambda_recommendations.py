"""
AWS Lambda Function: AI Product Recommendations
Deploy this on AWS Lambda + API Gateway

Steps:
1. Create Lambda function (Python 3.11)
2. Create API Gateway REST API
3. Add Cognito User Pool Authorizer to API Gateway
4. Connect GET /recommendations to this Lambda
"""

import json
import boto3
import random
from datetime import datetime


def lambda_handler(event, context):
    """
    Main Lambda handler - returns AI-powered product recommendations.
    JWT auth is handled by API Gateway Cognito Authorizer.
    """
    # Extract user identity from JWT claims (injected by Cognito Authorizer)
    user_id = event.get('requestContext', {}).get(
        'authorizer', {}).get('claims', {}).get('sub', 'anonymous')
    user_email = event.get('requestContext', {}).get(
        'authorizer', {}).get('claims', {}).get('email', '')

    print(f"[{datetime.now()}] Fetching recommendations for user: {user_email}")

    # In production: call Amazon Personalize or SageMaker here
    # recommendations = get_personalize_recommendations(user_id)
    recommendations = get_mock_ai_recommendations(user_id)

    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Authorization,Content-Type',
        },
        'body': json.dumps({
            'userId': user_id,
            'recommendations': recommendations,
            'generatedAt': datetime.now().isoformat(),
            'modelVersion': 'v1.2.0',
        })
    }


def get_mock_ai_recommendations(user_id: str) -> list:
    """
    Mock AI recommendations.
    In production: replace with Amazon Personalize / SageMaker call.
    """
    all_products = [
        {
            "id": "prod_001",
            "name": "Sony WH-1000XM5 Headphones",
            "description": "Industry-leading noise canceling with 30hr battery.",
            "price": 24990,
            "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400",
            "category": "Electronics",
            "rating": 4.8,
            "matchScore": round(random.uniform(0.90, 0.99), 2),
        },
        {
            "id": "prod_002",
            "name": "Nike Air Max 270",
            "description": "Bold look with unrivaled comfort for all-day wear.",
            "price": 9995,
            "imageUrl": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400",
            "category": "Footwear",
            "rating": 4.6,
            "matchScore": round(random.uniform(0.85, 0.95), 2),
        },
        {
            "id": "prod_003",
            "name": "Apple iPad Air M2",
            "description": "Supercharged by M2 chip with Liquid Retina display.",
            "price": 59900,
            "imageUrl": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=400",
            "category": "Electronics",
            "rating": 4.9,
            "matchScore": round(random.uniform(0.88, 0.97), 2),
        },
        {
            "id": "prod_004",
            "name": "Levi's 511 Slim Fit Jeans",
            "description": "Classic slim fit denim for everyday comfort.",
            "price": 3499,
            "imageUrl": "https://images.unsplash.com/photo-1542272604-787c3835535d?w=400",
            "category": "Clothing",
            "rating": 4.4,
            "matchScore": round(random.uniform(0.80, 0.92), 2),
        },
        {
            "id": "prod_005",
            "name": "Kindle Paperwhite",
            "description": "6.8\" display with warm light, waterproof, 10 weeks battery.",
            "price": 14999,
            "imageUrl": "https://images.unsplash.com/photo-1592496431122-2349e0fbc666?w=400",
            "category": "Electronics",
            "rating": 4.7,
            "matchScore": round(random.uniform(0.83, 0.94), 2),
        },
        {
            "id": "prod_006",
            "name": "Instant Pot Duo 7-in-1",
            "description": "Multi-cooker: pressure cooker, slow cooker and more.",
            "price": 8999,
            "imageUrl": "https://images.unsplash.com/photo-1585515320310-259814833e62?w=400",
            "category": "Kitchen",
            "rating": 4.5,
            "matchScore": round(random.uniform(0.78, 0.90), 2),
        },
    ]

    # Sort by match score (simulating AI ranking)
    sorted_products = sorted(all_products, key=lambda x: x['matchScore'], reverse=True)
    return sorted_products


def get_personalize_recommendations(user_id: str) -> list:
    """
    Production: Fetch from Amazon Personalize
    Uncomment and configure after setting up Personalize campaign.
    """
    # client = boto3.client('personalize-runtime', region_name='ap-south-1')
    # response = client.get_recommendations(
    #     campaignArn='arn:aws:personalize:ap-south-1:ACCOUNT_ID:campaign/product-recommendations',
    #     userId=user_id,
    #     numResults=10,
    # )
    # item_list = response['itemList']
    # # Fetch product details from DynamoDB for each itemId
    # return enrich_with_product_details(item_list)
    pass
