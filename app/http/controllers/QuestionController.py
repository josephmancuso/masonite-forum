''' A Module Description '''
from validator import Required, Not, Blank, validate, Length
from app.User import User
from app.Question import Question
from app.Vote import Vote

class QuestionController:
    ''' Class Docstring Description '''

    def show(self, Request):
        question = Question.find(Request.param('id'))
        return view('questions/show', {'question': question})

    def index(self):
        pass

    def create(self):
        return view('questions/new')

    def store(self, Request, Session):
        ok, errors = self.validate_input(Request.all())

        if not ok:
            display = ''
            for error in errors:
                display += '{0} {1} \n\n\n'.format(error.title(), errors[error][0])
            Session.flash('danger', display)
            return Request.redirect('/ask')
        
        Question.create(
            title=Request.input('title'),
            body=Request.input('body'),
            user_id=Request.user().id
        )
        Session.flash('success', 'Question added successfuly!')
        return Request.redirect('/')

    def questions(self, Request):
        questions = Question.where('user_id', Request.user().id).get()
        return view('questions/me', {'questions': questions})

    def upvote(self, Request, Session):
        id = Request.param('id')
        votes = Vote.where('question_id', id).where('user_id', Request.user().id).get()
        if votes.count() > 0:
            vote = votes.last()
            vote.value += 1
            if vote.value > 1:
                Session.flash('warning', 'Question already voted!')
            else:
                vote.save()
            return Request.redirect('/questions/@id', {'id': id})

        Vote.create(
            value=1,
            question_id=id,
            user_id=Request.user().id
        )
        return Request.redirect('/questions/@id', {'id': id})

    def downvote(self, Request, Session):
        id = Request.param('id')
        votes = Vote.where('question_id', id).where('user_id', Request.user().id).get()
        if votes.count() > 0:
            vote = votes.last()
            if vote.value == 1 or vote.value == 0:
                vote.value -= 1
                vote.save()
                return Request.redirect('/questions/@id', {'id': id})
            else:
                Session.flash('warning', 'Question already downvoted!')
                return Request.redirect('/questions/@id', {'id': id})
                
        Vote.create(
            value=1,
            question_id=id,
            user_id=Request.user().id
        )
        return Request.redirect('/questions/@id', {'id': id})

    def validate_input(self, data):
        rules = {
            'title': [Required, Not(Blank())],
            'body': [Required, Not(Blank())]
        }

        return validate(rules, data)