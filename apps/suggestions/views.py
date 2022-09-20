from django.shortcuts import render


class SuggestionsList(APIView):
    def get(self, request, format=None):
        suggestions = Suggestion.objects.all()
        serializer = SuggestionSerializer(suggestions, many=True)
        return Response(serializer.data)


class CreateSuggestion(APIView):
    def post(self, request, format=None):

        try:
            scope = [
                "https://spreadsheets.google.com/feeds",
                "https://www.googleapis.com/auth/spreadsheets",
                "https://www.googleapis.com/auth/drive.file",
                "https://www.googleapis.com/auth/drive",
            ]

            creds = ServiceAccountCredentials.from_json_keyfile_name(
                "gcp_key.json", scope
            )
            client = gspread.authorize(creds)
            gsheet = client.open("Psievidencia feedback").worksheet("Main")

            time = datetime.datetime.now()
            time = time.strftime("%m/%d/%Y %H:%M:%S")
            row = [time, request.data["title"], request.data["description"]]
            gsheet.append_row(row, 2)
        except HttpError as error:
            print(f"An error occurred: {error}")

        serializer = SuggestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
