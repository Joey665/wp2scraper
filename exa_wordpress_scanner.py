# exa_wordpress_scanner.py
import requests
import json
import time
from datetime import datetime

class ExaWordPressScanner:
    def __init__(self):
        self.api_key = "4fa472fa-f8be-4e5f-b683-f1a451871dc5"
        self.base_url = "https://api.exa.ai/search"
        self.credits_used = 0
        self.max_credits = 130
        
    def search_wordpress_vulnerabilities(self, domain):
        """
        Use Exa.ai to find vulnerability information about a specific domain
        """
        if self.credits_used >= self.max_credits:
            return None
            
        # Exa's semantic search - it understands context
        payload = {
            "query": f"WordPress security vulnerabilities on {domain} including CVE reports",
            "type": "neural",  # Neural search for better results
            "numResults": 10,
            "contents": {
                "text": True,
                "summary": True,
                "highlights": True
            }
        }
        
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            self.credits_used += 1
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract vulnerability info
                vulnerabilities = []
                for result in data.get('results', []):
                    text = result.get('text', '').lower()
                    title = result.get('title', '').lower()
                    
                    # Look for vulnerability indicators
                    vuln_indicators = [
                        'vulnerable', 'cve-', 'security issue',
                        'exploit', 'backdoor', 'sql injection',
                        'xss', 'cross-site scripting', 'privilege escalation'
                    ]
                    
                    found_vulns = []
                    for indicator in vuln_indicators:
                        if indicator in text or indicator in title:
                            found_vulns.append({
                                'type': indicator,
                                'summary': result.get('summary', ''),
                                'highlights': result.get('highlights', [])
                            })
                    
                    if found_vulns:
                        vulnerabilities.extend(found_vulns)
                
                return vulnerabilities
            else:
                print(f"❌ Exa API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error with Exa.ai: {e}")
            return None

    def analyze_site_security(self, url):
        """
        Use Exa.ai to analyze a site's overall security posture
        """
        if self.credits_used >= self.max_credits:
            return None
            
        payload = {
            "query": f"Security assessment of {url}: SSL, vulnerabilities, CMS, and security headers",
            "type": "neural",
            "numResults": 15,
            "contents": {
                "text": True,
                "summary": True
            }
        }
        
        headers = {
            'x-api-key': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(self.base_url, json=payload, headers=headers)
            self.credits_used += 1
            
            if response.status_code == 200:
                data = response.json()
                
                # Create a security profile
                security_profile = {
                    'ssl_info': self.extract_ssl_info(data),
                    'vulnerability_mentions': self.extract_vulnerabilities(data),
                    'security_headers': self.extract_security_headers(data),
                    'overall_risk': self.calculate_risk_score(data)
                }
                
                return security_profile
            else:
                print(f"❌ Exa API error: {response.status_code}")
                return None
                
        except Exception as e:
            print(f"❌ Error with Exa.ai: {e}")
            return None

    def extract_ssl_info(self, data):
        """
        Extract SSL/TLS information from search results
        """
        ssl_info = {}
        
        for result in data.get('results', []):
            text = result.get('text', '').lower()
            
            if 'ssl' in text or 'tls' in text or 'certificate' in text:
                # Parse SSL info
                if 'expired' in text:
                    ssl_info['expired'] = True
                if 'valid' in text:
                    ssl_info['valid'] = True
                if 'weak' in text or 'insecure' in text:
                    ssl_info['weak'] = True
        
        return ssl_info

    def extract_vulnerabilities(self, data):
        """
        Extract vulnerability mentions from search results
        """
        vulns = []
        
        for result in data.get('results', []):
            text = result.get('text', '').lower()
            
            # Check for CVE numbers
            import re
            cve_pattern = r'cve-\d{4}-\d{4,7}'
            cves = re.findall(cve_pattern, text)
            
            if cves:
                vulns.extend(cves)
            
            # Check for specific vulnerability types
            vuln_keywords = [
                'sql injection', 'xss', 'csrf', 'remote code execution',
                'privilege escalation', 'information disclosure'
            ]
            
            for keyword in vuln_keywords:
                if keyword in text:
                    vulns.append({
                        'type': keyword,
                        'context': text[:200] + '...'
                    })
        
        return vulns

    def calculate_risk_score(self, data):
        """
        Calculate a risk score based on Exa search results
        """
        score = 0
        risk_factors = 0
        
        for result in data.get('results', []):
            text = result.get('text', '').lower()
            
            # High risk indicators
            if any(word in text for word in ['critical', 'high severity', 'exploit available']):
                score += 20
                risk_factors += 1
            
            # Medium risk indicators
            if any(word in text for word in ['vulnerable', 'outdated', 'unsupported']):
                score += 10
                risk_factors += 1
            
            # Low risk indicators
            if any(word in text for word in ['update available', 'best practice']):
                score += 5
                risk_factors += 1
        
        # Normalize score
        if risk_factors > 0:
            score = min(score / risk_factors, 100)
        
        return score
