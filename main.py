from pypackage.manager import managment
import logging


logging.basicConfig(filename="logger.txt",level=logging.INFO)
logger = logging.getLogger(__name__)

mng = managment()

while True:
    logger.info("----------------------------------------------------------------")
    logger.info("FOR BOOKS: (ENTER)")
    logger.info("11 TO ADD\n12 FOR GET BOOK BY ID\n13 FOR GETTING ALL BOOKS\n14 TO UPDATE BOOK COPIES\n15 FOR SEARCHING BOOK THORUGH KEYWORD")
    logger.info("----------------------------------------------------------------")
    logger.info("FOR MEMBERS: (ENTER)")
    logger.info("21 TO ADD\n22 TO GET MEMBER BY ID\n23 FOR GETTING ALL MEMBERS")
    logger.info("----------------------------------------------------------------")
    logger.info("FOR LOANS: (ENTER)")
    logger.info("31 TO ADD LOAN RECORD\n32 FOR UPDATING STATUS OF LOAN\n33 FOR LISTING ALL ACTIVE LOANS\n34 FOR LISTING ALL OVER DUE LOANS")
    logger.info("----------------------------------------------------------------")
    logger.info("CHECKING DATA:(ENTER)")
    logger.info("41 FOR CHECKING TOP BORROWED BOOKS\n42 FOR GETTING BOROWING HISTORY OF A MEMBER\n43 FOR LISTING BOOKS NEVER BORROWED\n44 FOR CHECKING THE TOTALS OR EVERY TABLE")
    logger.info("ENTER 0 TO EXIT CODE!!! :")
    
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
                    logger.setLevel(logging.ERROR)
                    logger.error("INVALID NUMBER")
                    logger.setLevel(logging.INFO)
            except Exception as err:
                logger.setLevel(logging.ERROR)
                logger.error("ERROR:",err)
                logger.setLevel(logging.INFO)

            finally:
                pass

        case 22:
            member_id  = input("enter member id :")
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
            limit : int | str = input("enter the maximum limit of records to reterive:")
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
            data = mng.get_statistics()# - Return a dictionary with:
            logger.info(data)

        case 0:
            logger.info("EXITING CODE BLOCK!!!")
            break
        case _:
            logger.info("ENTER VALID OPTION!!!")



