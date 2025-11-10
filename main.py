from library_manager import managment

mng = managment()

while True:
    print("----------------------------------------------------------------")
    print("FOR BOOKS: (ENTER)")
    print("11 TO ADD\n12 FOR GET BOOK BY ID\n13 FOR GETTING ALL BOOKS\n14 TO UPDATE BOOK COPIES\n15 FOR SEARCHING BOOK THORUGH KEYWORD")
    print("----------------------------------------------------------------")
    print("FOR MEMBERS: (ENTER)")
    print("21 TO ADD\n22 TO GET MEMBER BY ID\n23 FOR GETTING ALL MEMBERS")
    print("----------------------------------------------------------------")
    print("FOR LOANS: (ENTER)")
    print("31 TO ADD LOAN RECORD\n32 FOR UPDATING STATUS OF LOAN\n33 FOR LISTING ALL ACTIVE LOANS\n34 FOR LISTING ALL OVER DUE LOANS")
    print("----------------------------------------------------------------")
    print("CHECKING DATA:(ENTER)")
    print("41 FOR CHECKING TOP BORROWED BOOKS\n42 FOR GETTING BOROWING HISTORY OF A MEMBER\n43 FOR LISTING BOOKS NEVER BORROWED\n44 FOR CHECKING THE TOTALS OR EVERY TABLE")
    print("ENTER 0 TO EXIT CODE!!! :")
    
    inp = 1
    try:
        inp = int(input())
    except Exception as err:
        pass

    match inp:
        case 11:
            title = input("enter title of book ")
            author = input("enter author of book ")
            published_year = input("enter published year ")
            copies = input("enter the available copies of the book ")
            mng.add_book(title, author, published_year, copies)

        case 12:
            book_id = input("enter book id ")
            mng.get_book_by_id(book_id) 

        case 13:

            mng.get_all_books()

        case 14:
            book_id = input("enter the book id ")
            copies = input("enter the number of book copies ")
            mng.update_book_copies(book_id, copies) 

        case 15:
            keyword = input("enter keyword for searching:")
            mng.search_books(keyword)
    
        
        case 21:
            name = input("enter name of member ")
            email = input("enter email address of the member ")
            phone = input("enter phone number of the number (11 digits) ")
            try:
                num = int(phone)
                if(len(phone) == 11):
                    mng.add_member(name, email, phone)
                else:
                    print("INVALID NUMBER")
            except Exception as err:
                print("ERROR:",err)
            finally:
                pass

        case 22:
            member_id = input("enter member id :")
            mng.get_member_by_id(member_id) # - Retrieve member details

        case 23:
            mng.get_all_members()  # - List all members

        case 31:
            book_id = int(input("Enter book id :"))
            member_id = int(input("Enter member id:"))
            days = input("enter days:")
            if not days:
                days = 14
            else:
                days = int(days) 
            mng.borrow_book(book_id, member_id, days) #- Create a loan record

        case 32:
            loan_id = input("enter loan id:")
            mng.return_book(loan_id)

        case 33:
            mng.get_active_loans()

        case 34:
            mng.get_overdue_loans()



        case 41:
            limit = input("enter the maximum limit of records to reterive:")
            if not limit:
                limit = 5
            else:
                limit = int(limit)
            mng.get_most_borrowed_books(limit)# - Return top borrowed books

        case 42:
            member_id = input("enter the member id:")
            mng.get_member_history(member_id) #- Get complete borrowing history for a member

        case 43:
            mng.get_books_never_borrowed()# - List books that have never been borrowed

        case 44:
            mng.get_statistics()# - Return a dictionary with:


        case 0:
            print("EXITING CODE BLOCK!!!")
            break
        case _:
            print("ENTER VALID OPTION!!!")



