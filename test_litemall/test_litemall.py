import requests
import pytest

from test_litemall.log import logger
import json


class TestLitemail:
    def setup_class(self):
        url_admin = "https://litemall.hogwarts.ceshiren.com/admin/auth/login"
        logindata_admin = {"username": "admin123",
                      "password":"admin123",
                      "code":""}
        r = requests.post(url =url_admin, json=logindata_admin)
        self.token = r.json()['data']['token']

        url_auth = "https://litemall.hogwarts.ceshiren.com/wx/auth/login"
        login_auth = {"username": "user123", "password":"user123"}
        r2 = requests.post(url =url_auth, json=login_auth)
        self.auth_token = r2.json()['data']['token']
        self.age = "18"


    def teardown(self):

        #-------执行命令会提示没有good_id 属性

        url = "https://litemall.hogwarts.ceshiren.com/admin/goods/delete"
        #delete_data = {"id": self.good_id}
        headers = {
            "X-Litemall-Admin-Token": self.token
                   }
        r = requests.post(url=url, json={"id": self.good_id}, headers=headers)
        logger.debug(f"删除商品的响应信息为{json.dumps(r.json(), indent=2, ensure_ascii=False)}")

    @pytest.mark.parametrize("goods_name, goods_number", [("赫本12号", "HJJ1015")])
    def test_add_goods(self, goods_name, goods_number):
        url = "https://litemall.hogwarts.ceshiren.com/admin/goods/create"
        goods_data = {"goods": {"picUrl": "", "gallery": [], "isHot": False, "isNew": True, "isOnSale": True, "goodsSn": goods_number, "name": goods_name, "counterPrice": "10"},
                  "specifications": [{"specification": "规格", "value": "标准", "picUrl": ""}],
                  "products": [{"id": 0, "specifications": ["标准"], "price": "20",  "number":"1000", "url":""}],
                  "attributes": []}

        headers = {
            "X-Litemall-Admin-Token": self.token
                   }
        r = requests.post(url=url, json=goods_data, headers=headers)
        logger.info(f"上架商品返回的响应内容为{json.dumps(r.json(), indent=2, ensure_ascii=False)}")
        assert r.json()['errmsg'] == "成功"

    '''加入到购物车'''
    @pytest.mark.parametrize("goods_name", ["赫本12号"])
    def test_add_cart(self, goods_name):

        url = "https://litemall.hogwarts.ceshiren.com/admin/goods/list"
        params = {"name": goods_name, "sort": "add_time", "order": "desc"}
        headers = {
            "X-Litemall-Admin-Token": self.token
                   }
        r = requests.get(url=url, params=params, headers=headers)
        self.good_id = r.json()['data']['list'][0]['id']

        url = "https://litemall.hogwarts.ceshiren.com/admin/goods/detail"
        params = {"id": self.good_id}
        headers = {
            "X-Litemall-Admin-Token": self.token
                   }
        r = requests.get(url=url, params=params, headers=headers)
        productid = r.json()['data']['products'][0]['id']


        url = "https://litemall.hogwarts.ceshiren.com/wx/cart/add"
        goods_data = {"goodsId": self.good_id, "number": 1, "productId": productid}
        headers = {
            "X-Litemall-Token": self.auth_token
                   }
        r = requests.post(url=url, json=goods_data, headers=headers)
        assert r.json()['errmsg'] == "成功"
        logger.info(f"加入购物车返回的响应内容为{json.dumps(r.json(), indent=2, ensure_ascii=False)}")
