import json
from langchain.schema import Document

class JobProfileParser:
    """
    A class to parse job profiles from a JSON file and convert them into LangChain Documents.
    """

    def __init__(self, file_path: str):
        """Initialize with the JSON file path."""
        self.file_path = file_path
        self.data = self.load_json()

    def load_json(self):
        """Load JSON data from a file."""
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def extract_general_info(self, job):
        """Extract general job information."""
        return {
            "job_role": job.get("jobRole", "N/A"),
            "sector": job.get("sector", "N/A"),
            "sub_sector": job.get("subSector", "N/A"),
            "college_category": job.get("collegeCategory", "N/A"),
            "experience_level": job.get("experienceLevel", "N/A"),
            "education_level": job.get("minEducationLevel", "N/A"),
            "job_location": job.get("jobLocation", "N/A"),
            "created_at": job.get("createdAt", [{}])[0].get("$date", "N/A"),
            "updated_at": job.get("updatedAt", {}).get("$date", "N/A"),
            "deleted": job.get("deleted", False),
            "job_role_key": job.get("jobRoleKey", "N/A"),
            "slug": job.get("slug", "N/A"),
            "generated_by": job.get("generatedBy", "N/A"),
            "language_code": job.get("languageCode", "N/A"),
        }

    def extract_job_profile(self, job):
        """Extract job profile details (Description & Day in the Life)."""
        job_profile = job.get("jobProfile", {})
        return {
            "description": job_profile.get("generalDescription", {}).get("text", "N/A"),
            "day_in_life": job_profile.get("dayInTheLife", {}).get("text", "N/A"),
            "reasons_liked": [item["reason"] for item in job_profile.get("reasonsLiked", [])],
            "reasons_disliked": [item["reason"] for item in job_profile.get("reasonsDisliked", [])],
            "prepare_for_role": {entry["key"]: entry["value"] for entry in job_profile.get("prepareForRole", [])},
        }

    def extract_list_items(self, job, key):
        """Extract list-based items like reasons liked/disliked."""
        return [item["reason"] for item in job.get("jobProfile", {}).get(key, [])]

    def extract_dict_items(self, job, key):
        """Extract dictionary-based items like aptitude ratings, interest ratings, value ratings."""
        return {
            entry["attribute"]: {"score": entry["score"], "reason": entry["reason"]}
            for entry in job.get(key, [])
        }

    def extract_employers(self, job):
        """Extract employer names."""
        return [
            employer["name"]
            for employer in job.get("employers", {}).get("wellKnownEmployers", [])
        ]

    def extract_geographic_details(self, job):
        """Extract geographic job details."""
        return [
            f"{geo['geographicOption']}: {geo['jobAvailability']} (Salary: {geo['estimatedSalaryRange']})"
            for geo in job.get("geographicJobDetails", [])
        ]

    def extract_career_pathways(self, job):
        """Extract career pathways."""
        return {
            pathway["pathwayTitle"]: pathway["description"]
            for pathway in job.get("careerPathways", [])
        }

    def extract_passions(self, job):
        """Extract job-related passions."""
        return [passion.get("passion", "N/A") for passion in job.get("allPassions", [])]

    def create_document(self, job):
        """Create a LangChain Document from a job entry."""
        general_info = self.extract_general_info(job)
        job_profile = self.extract_job_profile(job)

        # Generate document content
        content = f"""
        *Job Role*: {general_info['job_role']}
        *Sector*: {general_info['sector']}
        *Sub-Sector*: {general_info['sub_sector']}
        *College Category*: {general_info['college_category']}
        *Experience Level*: {general_info['experience_level']}
        *Minimum Education Level*: {general_info['education_level']}
        *Job Location*: {general_info['job_location']}

        *General Description*: {job_profile['description']}
        *Day in the Life*: {job_profile['day_in_life']}

        *Reasons People Like this Job*: {", ".join(job_profile['reasons_liked'])}
        *Reasons People Dislike this Job*: {", ".join(job_profile['reasons_disliked'])}

        *Preparation for the Role*:
        {json.dumps(job_profile['prepare_for_role'], indent=4)}

        *Aptitude Ratings*:
        {json.dumps(self.extract_dict_items(job, "aptitudeRatings"), indent=4)}

        *Interest Ratings*:
        {json.dumps(self.extract_dict_items(job, "interestRatings"), indent=4)}

        *Value Ratings*:
        {json.dumps(self.extract_dict_items(job, "valueRatings"), indent=4)}

        *Career Pathways*:
        {json.dumps(self.extract_career_pathways(job), indent=4)}

        *Employers*: {", ".join(self.extract_employers(job))}

        *Geographic Job Details*:
        {json.dumps(self.extract_geographic_details(job), indent=4)}

        *Passions*: {", ".join(self.extract_passions(job))}

        *Generated By*: {general_info['generated_by']}
        *Language Code*: {general_info['language_code']}
        *Job Role Key*: {general_info['job_role_key']}
        *Slug*: {general_info['slug']}

        *Created At*: {general_info['created_at']}
        *Updated At*: {general_info['updated_at']}
        *Deleted*: {general_info['deleted']}
        """

        metadata = {key: value for key, value in general_info.items() if key != "job_role"}

        return Document(page_content=content, metadata=metadata)

    def convert_to_documents(self):
        """Convert all job profiles into LangChain Documents."""
        return [self.create_document(job) for job in self.data]

# # Usage
# file_path = "/mnt/data/CareerAdvisoryService.job_profiles_en_100_6thFeb.json"
# parser = JobProfileParser(file_path)
# documents = parser.convert_to_documents()

# # Display first document as an example
# print(documents[0])