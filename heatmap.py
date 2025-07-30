from utils.chrome_driver import setup_chrome_driver

def capture_heatmap():
    """
    Capture liquidation heatmap using Chrome driver
    """
    try:
        # Initialize the Chrome driver with our custom settings
        driver = setup_chrome_driver()
        
        try:
            # Your existing heatmap capture code here
            # Example:
            # driver.get(your_heatmap_url)
            # driver.save_screenshot("heatmap.png")
            pass

        finally:
            # Always make sure to quit the driver
            driver.quit()
            
    except Exception as e:
        print(f"Error capturing heatmap: {str(e)}")
        raise
