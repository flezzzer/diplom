from locust import HttpUser, task, between

USER_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImRiYjQyNjFkLWUwMmItNGQ2MS04NzYyLWFmNmM2ZGFkYmVmOCIsImVtYWlsIjoic2hwb3QxMjFhLmRlbkBtYWlsLnJ1IiwiZXhwIjoxNzQ2NzkwNDg5fQ.Uy2kecCss9otKClYLoxYicR48rvZyWBzEAftL0wKC5I"
SELLER_TOKEN = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6IjRjYWFmNjY5LTRjZGUtNGFiNC04MmYyLTg4NTVjZDJlNmNhZCIsImVtYWlsIjoic2hwb3RhLmRlbkBtYWlsLnJ1IiwiZXhwIjoxNzQ2NzkwNDc3fQ.M1TOeErHYUpidqKkHTYSQUtm2dJ1TMzPWO6o0xD0iLE"
SELLER_ID = "4caaf669-4cde-4ab4-82f2-8855cd2e6cad"

class MyUser(HttpUser):
    wait_time = between(1, 2)

    def on_start(self):
        # Сохраняем оба токена для дальнейшего использования
        self.user_token = USER_TOKEN
        self.seller_token = SELLER_TOKEN

    @task
    def get_protected_data(self):
        headers = {"Authorization": self.user_token}  # Используем токен пользователя
        self.client.get("/products/8974610a-1753-42f0-83ac-9d1473a106cd", headers=headers)

    @task
    def get_general_statistics(self):
        headers = {"Authorization": self.seller_token}  # Используем токен продавца
        self.client.get(f"/sellers/{SELLER_ID}/statistics", headers=headers)

    @task
    def get_category_statistics(self):
        headers = {"Authorization": self.seller_token}  # Используем токен продавца
        self.client.get(f"/sellers/{SELLER_ID}/category-statistics", headers=headers)

    @task
    def get_product_statistics(self):
        headers = {"Authorization": self.seller_token}  # Используем токен продавца
        self.client.get(f"/sellers/{SELLER_ID}/product-statistics", headers=headers)

    @task
    def get_order_statistics_by_date(self):
        headers = {"Authorization": self.seller_token}  # Используем токен продавца
        self.client.get(f"/sellers/{SELLER_ID}/order-statistics-by-date", headers=headers)
