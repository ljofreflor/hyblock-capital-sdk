#!/usr/bin/env python3
"""
Test script to verify Hyblock Capital SDK installation
"""

def test_sdk_installation():
    print("=== Testing Hyblock Capital SDK Installation ===")
    
    try:
        # Test basic import
        import hyblock_capital_sdk
        print("✓ Library imported successfully!")
        
        # Test core components
        from hyblock_capital_sdk import ApiClient, Configuration, CatalogApi
        print("✓ Core components imported successfully!")
        
        # List available API classes
        print("\nAvailable API classes:")
        api_classes = [attr for attr in dir(hyblock_capital_sdk) if attr.endswith('Api')]
        for api_class in api_classes:
            print(f"  - {api_class}")
        
        # Test API client creation
        print("\nTesting API client creation...")
        config = Configuration()
        client = ApiClient(config)
        print("✓ API client created successfully!")
        
        # Test API instance creation
        catalog_api = CatalogApi(client)
        print("✓ API instance created successfully!")
        
        print("\n=== Installation Test Completed Successfully! ===")
        print("The Hyblock Capital SDK is properly installed and functional.")
        return True
        
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sdk_installation()
    exit(0 if success else 1)
