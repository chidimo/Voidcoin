from django.test import TestCase

# class SiteUserViewTests(TestCase):

#     def test_user_can_login(self):
#         goodlogin = self.client.post("/siteuser/login/", {"username" : "admin@choralcentral.com", "password" : "dwarfstar"})
#         self.assertEqual(goodlogin.status_code, 302) # my login page redirects
#         self.assertEqual(goodlogin["location"], "/siteuser/dashboard/")

#         badlogin = self.client.post("/siteuser/login/", {"username" : "admin@chin", "password" : "dwar"})
#         # self.assertEqual(badlogin.context["form.errors"], "Your username and password didn't match. Please try again.")
#         print(badlogin["form.errorss"])

#     def test_non_existent_user(self):
#         resp = self.client.get("/siteuser/10000/")
#         self.assertEqual(resp.status_code, 404)
#         # the line below will only pass if debug is set to false
#         self.assertTemplateUsed(response=resp, template_name="errors/404.html")

#     def test_get_dashboard(self):
#         resp = self.client.get("/siteuser/dashboard/")
#         self.assertEqual(resp.status_code, 200)
#         self.assertTrue("dashboard" in resp.context)
#         self.assertTemplateUsed(response=resp, template_name="siteuser/detail.html")
