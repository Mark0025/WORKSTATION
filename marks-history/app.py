import subprocess

class WisdomExtractor:
    def extract_wisdom(self, url):
        """Use Fabric (Go) to extract wisdom from video"""
        try:
            # Using Fabric's CLI directly
            cmd = ["fabric", "-y", url, "--pattern", "extract_wisdom", "--stream"]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.returncode == 0:
                return result.stdout
            else:
                print(f"Error extracting wisdom: {result.stderr}")
                return None
        except Exception as e:
            print(f"Error running Fabric: {e}")
            return None
