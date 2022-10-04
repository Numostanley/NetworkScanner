# import json
# from django.test import TestCase
# from apis.scanners.tools.wapiti import WapitiScanner


# class WapitiTest(TestCase):
    
#     def test_sslyze(self):
        
#         view = WapitiScanner('104.16.244.78').response()
        
#         print(view)
        
#         data = json.loads(view)
#         print(data[0])
        
#         self.assertEqual(isinstance(view, object), True)
