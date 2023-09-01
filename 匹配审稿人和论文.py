from bs4 import BeautifulSoup
import re


def extract_data_from_html(file_path):
    # Load the content of the file
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
    return BeautifulSoup(content, "html.parser")


def extract_papers_and_authors(paper_soup):
    # Extracting table data from the soup
    tables = paper_soup.find_all("table")
    rows = tables[0].find_all("tr")

    # Extracting data from the rows
    data = [list(map(lambda cell: cell.get_text().strip(), row.find_all("td"))) for row in rows[1:]]

    # Extracting titles and authors
    titles, authors = [], []
    for entry in [row[1] for row in data]:
        parts = entry.split("Research Papers")
        if len(parts) > 1:
            titles.append(parts[0].strip())
            authors.append(parts[1].split("DOI")[0].strip())
    return titles, authors


def extract_reviewer_names(reviewers_soup):
    # Using regex to extract two-word names from the reviewer list
    reviewer_names = []
    for elem in reviewers_soup.find_all("li"):
        text = elem.get_text().strip()
        match = re.match(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
        if match:
            reviewer_names.append(match.group(1))
    return reviewer_names


def find_papers_by_reviewers(titles, authors, reviewers):
    papers_by_reviewers = {}
    for reviewer in reviewers:
        for title, author_list in zip(titles, authors):
            if reviewer in author_list:
                if reviewer not in papers_by_reviewers:
                    papers_by_reviewers[reviewer] = []
                papers_by_reviewers[reviewer].append(title)
    return papers_by_reviewers


def main():
    # Extract data from HTML files
    paper_soup = extract_data_from_html("./论文列表.html")
    reviewers_soup = extract_data_from_html("./审稿人.html")

    # Extract titles and authors from the paper_soup
    titles, authors = extract_papers_and_authors(paper_soup)

    # Extract reviewers from the reviewers_soup
    reviewers = extract_reviewer_names(reviewers_soup)

    # Find papers authored by the reviewers
    papers_by_reviewers = find_papers_by_reviewers(titles, authors, reviewers)

    for reviewer, papers in papers_by_reviewers.items():
        print(f"{reviewer}:")
        for paper in papers:
            print(f"   - {paper}")
        print()


if __name__ == "__main__":
    main()
