import sys
import os

# Add the parent directory to sys.path so we can import backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from backend.main import get_insights
    print("Running get_insights()...")
    insights = get_insights()
    print("Success! Insights generated.")
    # print(insights) 
except Exception as e:
    print("Caught exception:")
    import traceback
    traceback.print_exc()
