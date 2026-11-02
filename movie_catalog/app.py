from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index_view():
    return render_template('index.html')


@app.route('/search')
def search_movie():
    title = request.args.get('title', '')
    cleaned_title = title.strip()

    if not cleaned_title:
        return render_template('result.html', heading='Укажите название', message='Название фильма не указано'), 400

    return render_template('result.html', heading='Ваш поисковый запрос', message=f'Вы искали фильм: {cleaned_title}')


@app.route('/review', methods=['POST'])
def add_review():
    title = request.form.get('title', '')
    rating = request.form.get('rating', '')
    review = request.form.get('review', '')

    cleaned_title = title.strip()
    cleaned_review = review.strip()

    if not cleaned_title or not cleaned_review:
        return render_template('result.html', heading='Проверьте отзыв', message='Название фильма и текст отзыва не могут быть пустыми'), 400

    try:
        rating = int(rating)
    except (ValueError, TypeError):
        return render_template('result.html', heading='Проверьте отзыв', message='Оценка должна быть целым числом'), 400

    if not 1 <= rating <= 5:
        return render_template('result.html', heading='Проверьте отзыв', message='Оценка должна быть от 1 до 5'), 400

    return render_template('result.html', heading='Спасибо за отзыв', message=f'Отзыв о фильме «{cleaned_title}» принят. Оценка: {rating}/5.')


if __name__ == '__main__':
    app.run()
