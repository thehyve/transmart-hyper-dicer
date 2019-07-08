POST_JSON_RESPONSES = {
    '/auth/realms/test/protocol/openid-connect/token':  {
        'access_token': '54604e3b-4d6a-419d-9173-4b1af0530bfb',
        'token_type': 'bearer',
        'expires_in': 42695,
        'scope': 'read write'},
    '/v2/observations': {
        'dimensionDeclarations': [
        {
            'name': 'study',
            'dimensionType': 'attribute',
            'sortIndex': 'null',
            'valueType': 'Object',
            'fields': [
                {
                    'name': 'name',
                    'type': 'String'
                }
            ]
        },
        {
            'name': 'concept',
            'dimensionType': 'attribute',
            'sortIndex': 'null',
            'valueType': 'Object',
            'fields': [
                {
                    'name': 'conceptPath',
                    'type': 'String'
                },
                {
                    'name': 'conceptCode',
                    'type': 'String'
                },
                {
                    'name': 'name',
                    'type': 'String'
                }
            ]
        },
        {
            'name': 'patient',
            'dimensionType': 'subject',
            'sortIndex': 1,
            'valueType': 'Object',
            'fields': [
                {
                    'name': 'id',
                    'type': 'Int'
                },
                {
                    'name': 'trial',
                    'type': 'String'
                },
                {
                    'name': 'inTrialId',
                    'type': 'String'
                },
                {
                    'name': 'subjectIds',
                    'type': 'Object'
                },
                {
                    'name': 'birthDate',
                    'type': 'Timestamp'
                },
                {
                    'name': 'deathDate',
                    'type': 'Timestamp'
                },
                {
                    'name': 'age',
                    'type': 'Int'
                },
                {
                    'name': 'race',
                    'type': 'String'
                },
                {
                    'name': 'maritalStatus',
                    'type': 'String'
                },
                {
                    'name': 'religion',
                    'type': 'String'
                },
                {
                    'name': 'sexCd',
                    'type': 'String'
                },
                {
                    'name': 'sex',
                    'type': 'String'
                }
            ]
        },
        {
            'name': 'visit',
            'dimensionType': 'attribute',
            'sortIndex': 'null',
            'valueType': 'Object',
            'fields': [
                {
                    'name': 'id',
                    'type': 'Int'
                },
                {
                    'name': 'activeStatusCd',
                    'type': 'String'
                },
                {
                    'name': 'startDate',
                    'type': 'Timestamp'
                },
                {
                    'name': 'endDate',
                    'type': 'Timestamp'
                },
                {
                    'name': 'inoutCd',
                    'type': 'String'
                },
                {
                    'name': 'locationCd',
                    'type': 'String'
                },
                {
                    'name': 'encounterIds',
                    'type': 'Object'
                }
            ]
        },
        {
            'name': 'start time',
            'dimensionType': 'attribute',
            'sortIndex': 'null',
            'valueType': 'Timestamp',
            'inline': 'true'
        },
        {
            'name': 'end time',
            'dimensionType': 'attribute',
            'sortIndex': 'null',
            'valueType': 'Timestamp',
            'inline': 'true'
        },
        {
            'name': 'location',
            'dimensionType': 'attribute',
            'sortIndex': 'null',
            'valueType': 'String',
            'inline': 'true'
        },
        {
            'name': 'trial visit',
            'dimensionType': 'attribute',
            'sortIndex': 'null',
            'valueType': 'Object',
            'fields': [
                {
                    'name': 'id',
                    'type': 'Int'
                },
                {
                    'name': 'relTimeLabel',
                    'type': 'String'
                },
                {
                    'name': 'relTimeUnit',
                    'type': 'String'
                },
                {
                    'name': 'relTime',
                    'type': 'Int'
                }
            ]
        },
        {
            'name': 'provider',
            'dimensionType': 'attribute',
            'sortIndex': 'null',
            'valueType': 'String'
        },
        {
            'name': 'sample_type',
            'dimensionType': 'null',
            'sortIndex': 'null',
            'valueType': 'String'
        },
        {
            'name': 'missing_value',
            'dimensionType': 'null',
            'sortIndex': 'null',
            'valueType': 'String'
        }
    ],
         'sort': [
        {
            'dimension': 'concept',
            'sortOrder': 'asc'
        },
        {
            'dimension': 'provider',
            'sortOrder': 'asc'
        },
        {
            'dimension': 'patient',
            'sortOrder': 'asc'
        },
        {
            'dimension': 'visit',
            'sortOrder': 'asc'
        },
        {
            'dimension': 'start time',
            'sortOrder': 'asc'
        }
    ],
         'cells': [
                {
                    'inlineDimensions': [
                        'null',
                        'null',
                        '@'
                    ],
                    'dimensionIndexes': [
                        0,
                        0,
                        0,
                        'null',
                        0,
                        'null',
                        'null',
                        'null',
                        'null',
                        'null',
                        'null',
                        'null'
                    ],
                    'numericValue': 20
                },
                {
                    'inlineDimensions': [
                        'null',
                        'null',
                        '@'
                    ],
                    'dimensionIndexes': [
                        0,
                        1,
                        0,
                        'null',
                        0,
                        'null',
                        'null',
                        'null',
                        'null',
                        'null',
                        'null',
                        'null'
                    ],
                    'stringValue': 'Caucasian'
                },
                {
                    'inlineDimensions': [
                        'null',
                        'null',
                        '@'
                    ],
                    'dimensionIndexes': [
                        0,
                        2,
                        0,
                        'null',
                        0,
                        'null',
                        'null',
                        'null'
                    ],
                    'stringValue': 'Female'
                }
            ],
         'dimensionElements': {
            'study': [
                {
                    'name': 'CATEGORICAL_VALUES'
                }
            ],
            'concept': [
                {
                    'conceptPath': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Age\\',
                    'conceptCode': 'CV:DEM:AGE',
                    'name': 'Age'
                },
                {
                    'conceptPath': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Race\\',
                    'conceptCode': 'CV:DEM:RACE',
                    'name': 'Race'
                },
                {
                    'conceptPath': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Gender\\Female\\',
                    'conceptCode': 'CV:DEM:SEX:F',
                    'name': 'Female'
                }
            ],
            'patient': [
                {
                    'id': -40,
                    'trial': 'CATEGORICAL_VALUES',
                    'inTrialId': '3',
                    'subjectIds': {
                        'SUBJ_ID': 'CV:40'
                    },
                    'birthDate': 'null',
                    'deathDate': 'null',
                    'age': 20,
                    'race': 'Caucasian',
                    'maritalStatus': 'null',
                    'religion': 'null',
                    'sexCd': 'Female',
                    'sex': 'female'
                }
            ],
            'visit': [],
            'trial visit': [
                {
                    'id': -30,
                    'relTimeLabel': '1',
                    'relTimeUnit': 'null',
                    'relTime': 'null',
                }
            ],
            'provider': [],
            'sample_type': [],
            'missing_value': [],
        }
    }
}

GET_JSON_RESPONSES = {
    'v2/...': {
    }

}