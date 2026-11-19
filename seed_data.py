from app import create_app
from app.extensions import db
from app.models import Food

app=create_app()

with app.app_context():
    if Food.query.first() is None:
        sample_food = [
            Food(foodname="Phở Bò Đặc Biệt", price=10,description="Phở bò tái nạm gầu nước dùng đậm đà gia truyền", image="pho_bo.jpg.png", category="Hauptspeise" ),
            Food(foodname="Bún chả", price=12, description="Bún chả nóng hổi vừa thổi vừa ăn", image="bun_cha.png", category ="Hauptspeise"),
            Food(foodname="Bánh mỳ", price=7, description="Bánh mỳ pate nhân đẫy đà", image="banh_my.png", category="Snack"),
            Food(foodname="Trà sữa", price=5, description="Hương trà đậm dà vị truyền thống", image="tra_sua.png", category="Getränkt")
        ]
        db.session.add_all(sample_food)
        db.session.commit()
        print("Added food into dataset")
    else:
        print("Dont need to add")