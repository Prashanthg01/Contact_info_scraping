def main():
    choice = input("Enter 1 for single page crawl or 2 for multiple page crawl: ")

    if choice == "1":
        import single_page_crawl
        single_page_crawl.main()
    elif choice == "2":
        import multiple_page_crawl
        multiple_page_crawl.main()
    else:
        print("Invalid choice. Please enter either 1 or 2.")

if __name__ == "__main__":
    main()
