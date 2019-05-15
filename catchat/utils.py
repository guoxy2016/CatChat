from flask import flash


def flash_errors(form):
    for field, errors in form.errors:
        for error in errors:
            flash('错误:<%s>:%s' % (field, error))
