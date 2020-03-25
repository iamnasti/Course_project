def query_1(sportX):
    ans = []
    query = (Sportsman.select(Coach.Name).join(Coach).filter(Sportsman.Sport_Name == sportX).group_by('Coach.Name'))
    for x in database.execute(query):
        ans.append(list(x))
    return ans

def query_2(substrX):
    ans = []
    query = (Training
         .select(Training.Target,
                 Training.Date,
                 Sportsman.Name,
                 Competition.Name)
         .join(M_Training)
         .join(Sportsman)
         .join(M_Competition)
         .join(Competition)
         .where(Competition.Name ** f'%{substrX}%')
         .order_by(Training.Date.desc()))
    for x in database.execute(query):
        ans.append(list(x))
    return ans

def query_3(duratX, titleY):
    ans = []
    query = (Fan
         .select(Fan.Club,
                 Sportsman.Name,
                 Competition.Date,
                 Competition.Name)
         .join(Sportsman)
         .join(M_Competition)
         .join(Competition)
         .switch(Sportsman)
         .join(M_Prize)
         .join(Prize)
         .where(Competition.Duration > duratX,
                Prize.Title == titleY)
         .group_by(Fan.Club)
         )
    for x in database.execute(query):
        ans.append(list(x))
    return ans