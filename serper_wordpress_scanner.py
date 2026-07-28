# serper_wordpress_scanner.py
import requests
import json
import time
from datetime import datetime

class SerperWordPressScanner:
    def __init__(self):
        self.api_key = "==="
        self.base_url = "https://google.serper.dev/search"
        
        # Advanced dorks optimized for finding vulnerable WordPress sites
        self.dorks = [
            # High-priority: Sites with known vulnerable plugins
            {
                'query': 'site:*.com "wp-content/plugins/wordfence" inurl:/wp-admin/',
                'priority': 'high',
                'plugins': ['wordfence']
            },
            {
                'query': 'site:*.com "wp-content/plugins/elementor" inurl:/wp-admin/',
                'priority': 'high',
                'plugins': ['elementor']
            },
            {
                'query': 'site:*.com "wp-content/plugins/yoast-seo" inurl:/wp-admin/',
                'priority': 'high',
                'plugins': ['yoast-seo']
            },
            {
                'query': 'site:*.com "wp-content/plugins/woocommerce" inurl:/wp-admin/',
                'priority': 'high',
                'plugins': ['woocommerce']
            },
            
            # Medium priority: Vulnerable themes
            {
                'query': 'intitle:"index of" wp-content/themes/twentytwenty',
                'priority': 'medium'
            },
            {
                'query': 'site:*.com "wp-content/themes/astra" inurl:/wp-admin/',
                'priority': 'medium'
            },
            
            # Low priority but easy targets
            {
                'query': 'inurl:/wp-content/uploads/ "index of"',
                'priority': 'low'
            },
            {
                'query': 'inurl:/wp-json/wp/v2/users/ "name" "id"',
                'priority': 'low'
            }
        ]
        
        self.queries_used = 0
        self.max_queries = 2400  # Leaving 100 for buffer

    def search(self, query, num_results=20):
        """
        Execute search using Serper API
        """
        if self.queries_used >= self.max_queries:
            print(f"⚠️ Query limit reached ({self.max_queries})")
            return []
        
        payload = json.dumps({
            "q": query,
            "num": num_results,
            "gl": "us",  # Country code
            "hl": "en"   # Language
        })
        
        headers = {
            'X-API-KEY': self.api_key,
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(self.base_url, headers=headers, data=payload)
            self.queries_used += 1
            
            if response.status_code == 200:
                data = response.json()
                results = []
                
                # Process organic results
                for result in data.get('organic', []):
                    results.append({
                        'url': result.get('link'),
                        'title': result.get('title'),
                        'snippet': result.get('snippet'),
                        'date': result.get('date', ''),
                        'source': 'serper'
                    })
                
                # Also check people also ask for more targets
                for result in data.get('peopleAlsoAsk', []):
                    if result.get('link'):
                        results.append({
                            'url': result.get('link'),
                            'title': result.get('question', ''),
                            'snippet': result.get('snippet', ''),
                            'source': 'serper'
                        })
                
                return results
            else:
                print(f"❌ Serper API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"❌ Error with Serper: {e}")
            return []

    def find_vulnerable_sites(self):
        """
        Run all dorks and collect targets
        """
        all_targets = []
        target_urls = set()  # Deduplication
        
        print(f"🔍 Starting Serper search with {len(self.dorks)} dorks...")
        
        for dork in self.dorks:
            print(f"  📡 Searching: {dork['query'][:50]}...")
            
            results = self.search(dork['query'])
            
            for result in results:
                url = result['url']
                if url and url not in target_urls:
                    target_urls.add(url)
                    
                    # Add plugin info if available
                    if dork.get('plugins'):
                        result['suspected_plugins'] = dork['plugins']
                    
                    result['priority'] = dork.get('priority', 'medium')
                    all_targets.append(result)
            
            # Be gentle with the rate limit
            time.sleep(2)
            
            # Check if we're running out of queries
            if self.queries_used >= self.max_queries:
                print(f"⚠️ Reached query limit. Found {len(all_targets)} targets.")
                break
        
        print(f"✅ Found {len(all_targets)} unique WordPress targets")
        return all_targets

    def check_plugins_in_snippet(self, target):
        """
        Parse snippet to identify potential plugins
        """
        snippet = target.get('snippet', '').lower()
        plugins_found = []
        
        common_plugins = [
            'wordfence', 'elementor', 'yoast-seo', 'woocommerce',
            'contact-form-7', 'jetpack', 'akismet', 'gravity-forms',
            'wp-rocket', 'yoast', 'advanced-custom-fields'
        ]
        
        for plugin in common_plugins:
            if plugin in snippet:
                plugins_found.append(plugin)
        
        return plugins_found

    def get_remaining_queries(self):
        """
        Get remaining Serper queries
        """
        return self.max_queries - self.queries_used
