from  app import app, render_template, request
import random
import randomname


@app.route('/')
@app.route('/home')
def home():
    filter_category = request.args.get('filter_category', default="all", type=str)
    products = []
    categories = [
        {
            'id': 1,
            'name': 'drink'
        },
        {
            'id': 2,
            'name': 'food'
        },
        {
            'id': 3,
            'name': 'fast food'
        },
        {
            'id': 4,
            'name': 'beer'
        },
        {
            'id': 5,
            'name': 'cafe'
        }
    ]
    for item in range(12):
        category = random.choice(categories)
        products.append({
            'id': 1,
            'name': randomname.get_name(noun=('food')),
            'price': 10,
            'discount': 30,
            'category_name': category['name'],
        })

    product_filter = []
    if filter_category == 'all' or filter_category == '':
        product_filter = products
    else:
        for product_found in products:
            if product_found['category_name'] == filter_category:
                product_filter.append(product_found)

    return render_template(
        'index.html',
        products=product_filter,
        category=categories,
        filter_category=filter_category
    )



@app.route('/product_detail/<string:name>/<string:category>/<string:price>/<string:image>')
def product_detail(name, category, price, image):
    return render_template('product_detail.html', name=name, category=category, price=price, image=image)