def parse_csv_line(line):
    """
    Parse a CSV line, considering commas within quotes.

    Parameters:
    line (str): A line from the CSV file.

    Returns:
    list: A list of fields parsed from the line.
    """
    fields = []
    field = ''
    in_quotes = False

    for char in line:
        if char == '"':
            in_quotes = not in_quotes
        elif char == ',' and not in_quotes:
            fields.append(field.strip())
            field = ''
        else:
            field += char

    fields.append(field.strip())
    return fields

def calculate_average_rating(file_path, certificate):
    """
    Calculate the average rating of movies with a specified certificate.

    Parameters:
    file_path (str): The path to the IMDB Movies dataset CSV file.
    certificate (str): The certificate to filter movies by.

    Returns:
    float: The average rating of movies with the specified certificate.
    """
    total_rating = 0
    count = 0

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Skip the header row
            next(file)
            
            for line in file:
                # Parse the line considering commas within quotes
                fields = parse_csv_line(line.strip())
                
                # Ensure we have enough fields
                if len(fields) > 7:
                    movie_certificate = fields[3].strip()
                    try:
                        rating = float(fields[7].strip())
                        if rating < 0 or rating > 10:
                            continue  # Skip invalid ratings
                    except ValueError:
                        continue  # Skip rows where the rating is not a valid float
                    
                    # Check if the certificate matches
                    if movie_certificate == certificate:
                        total_rating += rating
                        count += 1

        if count == 0:
            raise ValueError(f"No movies found with certificate: {certificate}")

        average_rating = total_rating / count
        return average_rating

    except FileNotFoundError:
        raise FileNotFoundError(f"The file at {file_path} was not found.")
    except IndexError:
        raise IndexError("The dataset does not contain the required columns.")
    except Exception as e:
        raise Exception(f"An error occurred: {e}")

# Example usage
file_path = r'C:/Users/sharo/OneDrive/Documents/Intro to informatics/imdb-movies-dataset.csv'
certificate = 'R'
try:
    average_rating = calculate_average_rating(file_path, certificate)
    print(f"Average rating for certificate '{certificate}': {average_rating}")
except Exception as e:
    print(e)