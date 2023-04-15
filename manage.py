import os
import math
import numpy as np
from PIL import Image
from datetime import timedelta
from flask import Flask,request,render_template,jsonify,session
from flask_bootstrap import Bootstrap

from mysql import *
from games import games

BASE_DIR=os.getcwd()

app=Flask(__name__)
app.permanent_session_lifetime = timedelta(days=7)
sem.permanent = True
bootstrap=Bootstrap(app)

def check_online():
    return 'Email' in session.keys()
def get_user(to_dict=True,userid=None):
    if userid!=None:
        user=sem.query(User).filter(User.Id==userid)
    else:
        email=session.get('Email')
        user=sem.query(User).filter(User.Email==email)
    if to_dict:
        user_dict=model_to_dict(user)
        return user_dict[0]
    return user.first()
def info_secret(user):
    user.pop('Id')
    user.pop('Password')
    return user
def my_info(secret=True):
    online=check_online()
    data={'online':online,'path':request.path}
    if online:
        user=get_user()
        if secret: user=info_secret(user)
        if user.get('Avatar')==None:
            user['Avatar']='../static/avatar/default/1.png'
        data['user']=user
        data['default_avatars']=default_avatars
    return data
def reject_offine():
    info=my_info(secret=False)
    data={'op':False,'online':info['online']}
    if info['online']==False:
        data['remark']='Please login first.'
        return (True,info,data)
    return (False,info,data)
def arange_comments(comments,col=None,page_max=0,page_vol=0,
        Sort=True,Cut=True,Page=True):
    if Sort and col:
        comments=sorted(comments, key=lambda x: x[col],reverse=True)
    if Cut and page_max and page_vol:
        comments=comments[:page_max*page_vol]
    if Page and page_vol:
        t=[]
        for page in range(page_max):
            t.append(comments[page*page_vol:(page+1)*page_vol])
        comments=t
    return comments
def get_comments(page_max=5,hot_vol=3,lat_vol=2,page_vol=5):
    path=request.path
    if path=='/': path='/index'
    if path=='/comment': path=request.form.get('path')
    comments=model_to_dict(sem.query(Comment).filter(Comment.Path==path))
    for comment in comments:
        comment['Likes']=sem.query(Like).filter_by(To=comment['Id']).count()
        commenter=get_user(userid=comment['From'])
        comment['Name']=commenter['Name']
        comment['Avatar']=commenter['Avatar']
        comment['Belong']=False
        user=my_info(secret=False)
        if user['online']:
            user=user['user']
            search=sem.query(Like).filter_by(
                To=comment['Id'],
                From=user['Id']
            )
            comment['Like']=bool(search.count())
            if user['Id']==comment['From']:
                comment['Belong']=True
    leng=len(comments)
    page_max=min(leng//page_vol+1,page_max)
    hottest=arange_comments(comments,'Likes',page_max,page_vol)
    latest=arange_comments(comments,'Time',page_max,page_vol)
    hoti,lati=0,0
    review=[]
    while(hoti<leng or lati<leng):
        for comment in hottest[hoti:hoti+hot_vol]:
            if comment not in review:
                review.append(comment)
        hoti+=hot_vol
        for comment in latest[lati:lati+lat_vol]:
            if comment not in review:
                review.append(comment)
        lati+=lat_vol
    review=arange_comments(comments,None,page_max,page_vol,Sort=False,Cut=True,Page=True)
    return (page_max,[('review',review),('hottest',hottest),('latest',latest)])
def show_comments():
    data={}
    page_max,data['comments']=get_comments()
    data['page_max']=page_max
    data['page_range']=range(1,page_max+1)
    return data
def center_cut(url):
    img=np.array(Image.open(url))
    row,col=img.shape[0:2]
    if row==col: return
    mi,ma=sorted(img.shape[0:2])
    size=(ma-mi)//2
    cut=img[size:mi+size,:] if row>col else img[:,size:mi+size]
    Image.fromarray(cut).save(url)

@app.route('/')
def index():
    data=my_info()
    techs=model_to_dict(sem.query(Tech))
    games=model_to_dict(sem.query(Game))
    data['techs']=techs[:6]
    data['games']=games[:4]
    data.update(show_comments())
    return render_template('index.html',**data)

@app.route('/games/<obj>')
def game(obj):
    reject,info,data=reject_offine()
    if reject: return jsonify(data)
    print('@@@@@game')
    print(obj)
    data.update(games.game_data(obj,info))
    data.update(my_info())
    data.update(show_comments())
    return render_template('games/'+obj+'.html',**data)

@app.route('/login',methods=['POST'])
def login():
    data={'remark':'The account was not found.'}
    user=model_to_dict(sem.query(User).filter(User.Email==request.form.get('Email')))
    if len(user)==1:
        user=user[0]
        if user['Password']==request.form.get('Password'):
            session['Email']=user['Email']
            user=get_user(False)
            user.Lastlogin=datetime.now()
            sem.commit()
            data['remark']='Login succeeded!'
        else: data['remark']='Password error'
    data.update(my_info())
    return jsonify(data)
    
@app.route('/register',methods=['POST'])
def register():
    email=request.form.get('Email')
    name=request.form.get('Name')
    password=request.form.get('Password')
    user=sem.query(User).filter(User.Email==email).first()
    if user==None:
        user=User(Email=email,Name=name,Password=password)
        sem.add(user)
        sem.commit()
        session['Email']=email
        user=model_to_dict(user)
        data=my_info()
        data['remark']='Your account was successfully registered!'
    else:
        data=my_info()
        data['remark']='This email has been registered.'
    return jsonify(data)

@app.route('/update',methods=['POST'])
def update():
    reject,info,data=reject_offine()
    if reject: return jsonify(data)
    obj=request.form.get('obj')
    data['remark']='Update failed.'
    if obj=='Name':
        user=get_user(False)
        user.Name=request.form.get('Name')
        sem.commit()
        data['op']=True
        data['remark']='Update succeeded!'
    if obj=='Password':
        oldpassword=request.form.get('OldPassword')
        password=get_user()['Password']
        if oldpassword==password:
            user=get_user(False)
            user.Password=request.form.get('NewPassword')
            sem.commit()
            data['op']=True
            data['remark']='Update succeeded!'
        else: data['remark']='Old password error.'
    if obj=='Notify':
        notify=request.form.get('Notify')
        if notify!=None and notify in ('1','2','3'):
            user=get_user(False)
            user.Notify=notify
            sem.commit()
            data['op']=True
            data['remark']='Update succeeded!'

    return jsonify(data)

@app.route('/exit',methods=['GET'])
def exit():
    if session.get('Email'):
        session.pop('Email')
    return jsonify()

@app.route('/upload',methods=['POST'])
def upload():
    reject,info,data=reject_offine()
    if reject: return jsonify(data)
    obj=request.form.get('obj')
    data['remark']='No such operation.'
    if obj=='Avatar':
        file=request.files.get('file')
        if file!=None:
            ext=file.filename.split('.')[-1]
            avatar_url='/static/avatar/'+str(info['user']['Id'])+'.'+ext
            url=BASE_DIR+avatar_url
            file.save(url)
            center_cut(url)
            user=get_user(False)
            user.Avatar='..'+avatar_url
            sem.commit()
            data['op']=True
            data['remark']='Upload succeeded!'
        else: data['remark']='No file received.'
    if obj=='default_avatar':
        url=request.form.get('url')
        content_url=url.replace('../../','../')
        if content_url in default_avatars:
            user=get_user(False)
            user.Avatar=content_url
            sem.commit()
            data['op']=True
            data['remark']='Upload succeeded!'
            data['url']=url
            data['content_url']=content_url
        else: data['remark']='Url error.'
    return jsonify(data)
@app.route('/comment',methods=['POST'])
def comment():
    reject,info,data=reject_offine()
    if reject: return jsonify(data)
    op=request.form.get('op')
    data['remark']='No such operation.'
    if op=='send':
        content=request.form.get('comment')
        comment=Comment(Content=content,Path=request.form.get('path'),From=info['user']['Id'])
        sem.add(comment)
        sem.commit()
        data['op']=True
        data['remark']='Sending succeeded!'
    if op=='delete':
        commentid=request.form.get('Id')
        userid=info['user']['Id']
        comment=sem.query(Comment).filter_by(Id=commentid,From=userid)
        if comment.count()==1:
            likes=sem.query(Like).filter_by(To=commentid)
            if likes.count()>0:
                likes.delete()
            comment.delete()
            sem.commit()
            data['op']=True
            data['remark']='Delete completed.'
        else:
            data['op']=False
            data['remark']='The comment was not found.'
    return jsonify(data)

@app.route('/like',methods=['POST'])
def like():
    reject,info,data=reject_offine()
    if reject: return jsonify(data)
    op=request.form.get('op')
    commentid=request.form.get('Id')
    userid=info['user']['Id']
    if op=='like':
        record=model_to_dict(sem.query(Like).filter_by(To=commentid,From=userid))
        if len(record)==0:
            like=Like(To=commentid,From=userid)
            sem.add(like)
            sem.commit()
            data['op']=True
        else: data['remark']='operation failed.'
    elif op=='nolike':
        sem.query(Like).filter_by(To=commentid,From=userid).delete()
        sem.commit()
        data['op']=True
    if data['op']:
        data['Likes']=sem.query(Like).filter_by(To=request.form.get('Id')).count()
    return jsonify(data)

@app.route('/<obj>')
def display(obj):
    data=my_info()
    if obj=='index': return index()
    return render_template(obj+'.html',**data)

app.secret_key=os.urandom(30)

if __name__=='__main__':
    app.run(debug = True)