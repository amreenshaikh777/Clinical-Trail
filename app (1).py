from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Welcome to the Clinical Trials API!"

@app.route('/trials', methods=['GET'])
def get_trials():
    condition = request.args.get('condition')
    sponsor = request.args.get('sponsor')
    
    if not condition or not sponsor:
        return jsonify({'error': 'Please provide both condition and sponsor parameters.'}), 400
    
    trials_data = fetch_clinical_trials(condition, sponsor)
    return jsonify(trials_data)

def fetch_clinical_trials(condition, sponsor):
    url = 'https://clinicaltrials.gov/api/v2/studies'
    parameters = {
        'query.cond': condition,
        'query.spons': sponsor,
        'fields': 'DesignInterventionModel,BriefSummary,CollaboratorName,CompletionDate,LocationCity,Condition,'
                  'PrimaryOutcomeTimeFrame,SecondaryOutcomeTimeFrame,PrimaryCompletionDate,OtherOutcomeMeasure,'
                  'ArmsInterventionsModule,MinimumAge,StudyFirstPostDate,OverallStatus,OtherOutcomeDescription,Sex,'
                  'SecondaryOutcomeMeasure,OtherOutcomeTimeFrame,LocationState,EnrollmentCount,StudyType,'
                  'LocationCountry,PrimaryOutcomeDescription,InterventionType,BriefTitle,StdAge,Phase,'
                  'DesignPrimaryPurpose,LeadSponsorClass,LeadSponsorName,Acronym,PrimaryOutcomeMeasure,NCTId,'
                  'LocationZip,DesignAllocation,HasResults,SecondaryOutcomeDescription,InterventionName,'
                  'DesignWhoMasked,StartDate,LocationFacility,LargeDocFilename,OrgStudyId,MaximumAge,LargeDocLabel,'
                  'EligibilityCriteria,LastUpdatePostDate,SecondaryId,DesignMasking,ResultsFirstSubmitDate',
        'format': 'json',
        'pageSize': 1000
    }
    all_trials = []
    next_page_token = None
    
    while True:
        if next_page_token:
            parameters['pageToken'] = next_page_token
        
        response = requests.get(url, params=parameters)
        data = response.json()
        
        all_trials.extend(data.get('studies', []))
        
        next_page_token = data.get('nextPageToken')
        if not next_page_token:
            break
    
    return all_trials

if __name__ == '__main__':
    app.run(debug=True)