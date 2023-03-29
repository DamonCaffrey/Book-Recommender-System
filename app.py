from flask import Flask,render_template,request
import pickle
import pandas
import numpy as np
import random

popular = pickle.load(open('popular_186_df.pkl','rb'))
pt_item_based = pickle.load(open('pt_item_based.pkl','rb'))
books = pickle.load(open('books_1072_df.pkl','rb'))
similarity_scores_item_based = pickle.load(open('similarity_scores_item_based.pkl','rb'))

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html',
                            book_name = list(popular['Book-Title'].values),
                            book_author = list(popular['Book-Author'].values),
                            votes = list(popular['Count-Ratings'].values),
                            ratings = list(popular['Average-Rating'].values),
                            image = list(popular['Image-URL-M'].values))

@app.route('/library')
def library_ui():
    return render_template('library.html')

@app.route('/library_books', methods=['post'])
def show_books():
    user_input = request.form.get('user_input')
    data = []
    
    idx_book = random.choice(list(range(len(books))))
    for i,x in enumerate(books['Book-Title']):
        if x.lower() == user_input.lower():
            idx_book = i
            break
    
    item = []
    item.append(books['Book-Title'][idx_book])
    item.append(books['Book-Author'][idx_book])
    item.append(books['ISBN'][idx_book])
    item.append(books['Year-Of-Publication'][idx_book])
    item.append(books['Publisher'][idx_book])
    item.append(books['Image-URL-M'][idx_book])
    item.append(books['Synopsis'][idx_book])
    item.append(books['Average-Rating'][idx_book])
    item.append(books['Count-Ratings'][idx_book])
    data.append(item)

    
    book_author = books['Book-Author'][idx_book]
    book_title = books['Book-Title'][idx_book]

    for i in range(5):
        item = []
        idx = random.choice(list(range(len(popular))))

        item.append(popular['Book-Title'][idx])
        item.append(popular['Book-Author'][idx])
        item.append(popular['Image-URL-M'][idx])

        data.append(item)
    
    
    idx_pt = -1
    for i,x in enumerate(pt_item_based.index):
        if x == book_title:
            idx_pt = i
            break
    
    similar_items = sorted(list(enumerate(similarity_scores_item_based[idx_pt])), key = lambda x:x[1], reverse = True)[1:6]
    
    for i in similar_items : 
        item = []
        temp_df = books[books["Book-Title"] == pt_item_based.index[i[0]]]
        
        item.append(temp_df['Book-Title'].iloc[0])
        item.append(temp_df['Book-Author'].iloc[0])
        item.append(temp_df['Image-URL-M'].iloc[0])
        data.append(item)
    
    count = len(books[books['Book-Author'] == book_author])

    if count >= 5 :

        temp_df = books[books['Book-Author'] == book_author].sort_values(by='Average-Rating', ascending=False)
        for i in range(5) :
            item = []
            
            item.append(temp_df['Book-Title'].iloc[i])
            item.append(temp_df['Book-Author'].iloc[i])
            item.append(temp_df['Image-URL-M'].iloc[i])

            print(item)
            data.append(item)

    print(count)
    return render_template('library.html', data = data)


@app.route('/recommend')
def recommend_ui():
    return render_template('recommend.html')

@app.route('/recommend_books', methods=['post'])
def recommend():
    user_input = request.form.get('user_input')
    
    idx = 0
    for i,x in enumerate(pt_item_based.index):
        if x.lower() == user_input.lower():
            idx = i
            break
    
    similar_items = sorted(list(enumerate(similarity_scores_item_based[idx])), key = lambda x:x[1], reverse = True)[1:6]
    
    data = []
    for i in similar_items : 
        item = []
        temp_df = books[books["Book-Title"] == pt_item_based.index[i[0]]]
        
        item.append(temp_df['Book-Title'].iloc[0])
        item.append(temp_df['Book-Author'].iloc[0])
        item.append(temp_df['Image-URL-M'].iloc[0])
        data.append(item)
    
    return render_template('recommend.html', data=data)

if __name__ == "__main__":
    app.run(debug=True, port=8000)