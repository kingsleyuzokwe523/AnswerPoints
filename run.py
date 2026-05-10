from app import create_app
import sys
import traceback

try:
    app = create_app()
    print("App created successfully!")
except Exception as e:
    print(f"ERROR: {e}")
    traceback.print_exc()
    sys.exit(1)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)