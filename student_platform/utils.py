def filter_student_lessons(obj):
    result = []
    for item in obj:
        result.append(
            {
                'id': item['article']['id'],
                'title': item['article']['title'],
                'quiz_score': item['article']['quiz_score'],
                'lock': item['lock'],
                'finished': item['finished'],
            }
        )
    return result
