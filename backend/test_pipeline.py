from pipeline import analyze_document

pdf_path = "sample_docs/Online_Shopping_System_SRS.pdf"

print("=" * 60)
print("COMPLETE PIPELINE")
print("=" * 60)

results = analyze_document(pdf_path)

print()

print("Total Requirements Analysed :", len(results))

print()

for result in results[:3]:

    print("=" * 60)

    print("Requirement ID :", result["id"])

    print()

    print("Requirement :")

    print(result["text"])

    print()

    print("Analysis :")

    print(result["analysis"])

    print("=" * 60)