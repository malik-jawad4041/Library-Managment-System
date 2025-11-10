from database import con
import datetime as dt
import psycopg2



# add the .commit() and .rollback() method

class managment:


    def __init__(self):
        self.conn = con.connect()




    def add_book(self,title, author, published_year, copies):
        try:
            cur = self.conn.cursor()
            cur.execute("insert into library.books (title,author,published_year,available_copies) values(%s,%s,%s,%s)",
                        (title,author,published_year,copies))
            self.conn.commit()
            print("BOOK ADDED SUCCESSFULLY :)")

        except psycopg2.Error as err:
            self.conn.rollback()
            print("ERROR!!:",err)
        finally:
            cur.close()



    




    def get_book_by_id(self,book_id): # Retrieve book details

        
        try:
            cur = self.conn.cursor()
            cur.execute("select * from library.books where book_id = %s",
                        (book_id,))
            data = cur.fetchall()
            print(data)

        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()







    def get_all_books(self): # List all books
         
        try:
            cur = self.conn.cursor()
            cur.execute("select book_id,title,author,published_year,available_copies from library.books")
            data = cur.fetchall()
            print(data)

        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()
    
    
    



    def update_book_copies(self,book_id, copies): # Update available copies
       
        try:
            cur = self.conn.cursor()
            cur.execute("update library.books set available_copies = %s where book_id = %s",(copies,book_id))
            self.conn.commit()            
            print("UPDATE SUCCESSFULL !!")

        except psycopg2.Error as err:
            self.conn.rollback()
            print("ERROR!!:",err)

        finally:
            cur.close()
    





    def search_books(self,keyword): # Search books by title or author


        keyword = f"%{keyword}%"
        try:
            cur = self.conn.cursor()
            cur.execute("select * from library.books where title ilike %s or author ilike %s",(keyword,keyword) )
            data = cur.fetchall()
            print(data)

        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()




#Members Management:

    def add_member(self,name, email, phone): #- Register a new member
        
        try:
            cur = self.conn.cursor()
            cur.execute("insert into library.members (name,email,phone) values(%s,%s,%s)",(name,email,phone) )
            self.conn.commit()

            print("DATA INSERTED SUCCESSFULLY!!")

        except psycopg2.Error as err:
            self.conn.rollback()
            print("ERROR!!:",err)

        finally:
            cur.close()







    def get_member_by_id(self,member_id): # - Retrieve member details

        try:
            cur = self.conn.cursor()
            cur.execute("select * from library.members where member_id = %s",(member_id,) )
            print(cur.fetchall())

        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()





    def get_all_members(self):  # - List all members

        try:
            cur = self.conn.cursor()
            cur.execute("select * from library.members" )
            print(cur.fetchall())

        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()







    #Loans Management:

    def borrow_book(self,book_id, member_id, days=14): #- Create a loan record
       
        date = dt.date.today() + dt.timedelta(days=days)
        try:
            cur = self.conn.cursor()
            cur.execute("insert into library.loans (book_id,member_id,due_date,status) values (%s,%s,%s,%s)",(book_id,member_id,date,"active") )
            self.conn.commit()            
            print("DATA INSERTED IN LOANS TABLE!!!")

        except psycopg2.Error as err:
            self.conn.rollback()
            print("ERROR!!:",err)

        finally:
            cur.close()







    def return_book(self,loan_id): # - Mark book as returned
       
        try:
            cur = self.conn.cursor()
            cur.execute("update library.loans set status = 'returned' where loan_id = %s",(loan_id,) )
            print("UPDATED LOANS TABLE!!!")
            self.conn.commit()

        except psycopg2.Error as err:
            self.conn.rollback()
            print("ERROR!!:",err)

        finally:
            cur.close()





    def get_active_loans(self): #- List all active loans
        
        try:
            cur = self.conn.cursor()
            cur.execute("select * from library.loans where status = 'active' " )
            print(cur.fetchall())

        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()




    def get_overdue_loans(self): #- List overdue loans
        
        date = dt.date.today()
        try:
            cur = self.conn.cursor()
            cur.execute("select * from library.loans where due_date < %s ",(date,) )
            print(cur.fetchall())
            
        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()







    def get_most_borrowed_books(self,limit=5):# - Return top borrowed books
        
        try:
            cur = self.conn.cursor()
            cur.execute(''' 
                select lb.book_id,title,author,published_year from
                library.books as lb inner join (select book_id from
                library.loans group by book_id order by 
                count(book_id) desc limit %s) as bk on lb.book_id = bk.book_id''',
                (limit,) )
            
            print(cur.fetchall())
            
        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()



    
    def get_member_history(self,member_id) :#- Get complete borrowing history for a member
        try:
            cur = self.conn.cursor()
            cur.execute("select * from library.loans where member_id = %s",(member_id,) )
            print(cur.fetchall())
            
        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()


    def get_books_never_borrowed(self):# - List books that have never been borrowed
        try:
            cur = self.conn.cursor()
            cur.execute('''select tb1.book_id,title,author,published_year from 
                        library.books as tb1 where tb1.book_id not in 
                        (select book_id from library.loans group by book_id)''')
            
            print(cur.fetchall())
            
        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()



    def get_statistics(self):# - Return a dictionary with:
        try:
            cur = self.conn.cursor()
            cur.execute('''with cte as (
    select count(*) as count, member_id
    from library.loans
    group by member_id
),
cte2 as (
    select status, count(status) as count
    from library.loans
    group by status
)
select 
    (select count(book_id) from library.books) as total_books,
    (select count(member_id) from library.members) as total_members,
    (select count from cte2 where status = 'active') as active_loans,
    (select member_id from cte where count = (select max(count) from cte) limit 1) as most_active_member;
''')
            
            result = cur.fetchall()       # will add dictionary format later
            dict = {
                'Total books':result[0][0],
                'total members':result[0][1],
                'active loans':result[0][2],
                'most active member"s id':result[0][3]
            }
            print(dict)

        except psycopg2.Error as err:
            print("ERROR!!:",err)

        finally:
            cur.close()

    def __del__(self):
        con.disconnect(self.conn)

      


'''
Total books
Total members
Active loans
Overdue loans
Most active member
'''











    