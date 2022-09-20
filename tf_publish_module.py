token = "<token_info>"
org = "<org_info>"
headers = {"Content-Type": "application/vnd.api+json", "Authorization" : "Bearer " + token }
module_name = "terraform-azurerm-resource-group"
provider = "azurerm"
version = "v0.0.1"

#Zip Module as package
subprocess.call(['tar', '-zcvf', "module.tar.gz", ".", "--exclude", "*.py"])

# Create Module
create_mod_url = "https://app.terraform.io/api/v2/organizations/"+ org +"/registry-modules"
data_load={'data': {'type':'registry-modules', 'attributes': {'name':module_name, "provider": provider, "registry-name":"private"}}}
data2=json.dumps(data_load)
requests.post(create_mod_url, headers=headers,data=data2)

#Create Module Version
create_mod_ver_url = "https://app.terraform.io/api/v2/organizations/"+ org +"/registry-modules/private/" + org + "/" + module_name + "/" + provider + "/versions"
data_load={'data': {'type':'registry-module-versions', 'attributes': {'version':version}}}
data2=json.dumps(data_load)
response = requests.post(create_mod_ver_url, headers=headers,data=data2)
version_response = json.loads(response.text)

#Publish Module
create_mod_pckg_url = version_response["data"]["links"]["upload"]
headers = {"Content-Type": "application/octet-stream"}
tar_data = open('./module.tar.gz', 'rb').read()
response = requests.put(create_mod_pckg_url, headers={'Content-Type': 'application/octet-stream'},data=tar_data )
