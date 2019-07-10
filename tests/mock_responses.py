POST_JSON_RESPONSES = {
    '/auth/realms/test/protocol/openid-connect/token': {
        'access_token': '54604e3b-4d6a-419d-9173-4b1af0530bfb',
        'token_type': 'bearer',
        'expires_in': 42695,
        'scope': 'read write'},
    '/v2/observations': {
        'dimensionDeclarations': [{
            'name': 'study',
            'dimensionType': 'attribute',
            'sortIndex': None,
            'valueType': 'Object',
            'fields': [
                {
                    'name': 'name',
                    'type': 'String'
                }
            ]
        }, {
            'name': 'concept',
            'dimensionType': 'attribute',
            'sortIndex': None,
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
        }, {
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
        }, {
            'name': 'visit',
            'dimensionType': 'attribute',
            'sortIndex': None,
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
        }, {
            'name': 'start time',
            'dimensionType': 'attribute',
            'sortIndex': None,
            'valueType': 'Timestamp',
            'inline': 'true'
        }, {
            'name': 'end time',
            'dimensionType': 'attribute',
            'sortIndex': None,
            'valueType': 'Timestamp',
            'inline': 'true'
        }, {
            'name': 'location',
            'dimensionType': 'attribute',
            'sortIndex': None,
            'valueType': 'String',
            'inline': 'true'
        }, {
            'name': 'trial visit',
            'dimensionType': 'attribute',
            'sortIndex': None,
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
        }, {
            'name': 'provider',
            'dimensionType': 'attribute',
            'sortIndex': None,
            'valueType': 'String'
        }, {
            'name': 'sample_type',
            'dimensionType': None,
            'sortIndex': None,
            'valueType': 'String'
        }, {
            'name': 'missing_value',
            'dimensionType': None,
            'sortIndex': None,
            'valueType': 'String'
        }],
        'sort': [{
            'dimension': 'concept',
            'sortOrder': 'asc'
        }, {
            'dimension': 'provider',
            'sortOrder': 'asc'
        }, {
            'dimension': 'patient',
            'sortOrder': 'asc'
        }, {
            'dimension': 'visit',
            'sortOrder': 'asc'
        }, {
            'dimension': 'start time',
            'sortOrder': 'asc'
        }],
        'cells': [{
                    'inlineDimensions': [
                        None,
                        None,
                        '@'
                    ],
                    'dimensionIndexes': [
                        0,
                        0,
                        0,
                        None,
                        0,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None
                    ],
                    'numericValue': 20
                },
                {
                    'inlineDimensions': [
                        None,
                        None,
                        '@'
                    ],
                    'dimensionIndexes': [
                        0,
                        1,
                        0,
                        None,
                        0,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None,
                        None
                    ],
                    'stringValue': 'Caucasian'
                },
                {
                    'inlineDimensions': [
                        None,
                        None,
                        '@'
                    ],
                    'dimensionIndexes': [
                        0,
                        2,
                        0,
                        None,
                        0,
                        None,
                        None,
                        None
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
                    'birthDate': None,
                    'deathDate': None,
                    'age': 20,
                    'race': 'Caucasian',
                    'maritalStatus': None,
                    'religion': None,
                    'sexCd': 'Female',
                    'sex': 'female'
                }
            ],
            'visit': [],
            'trial visit': [
                {
                    'id': -30,
                    'relTimeLabel': '1',
                    'relTimeUnit': None,
                    'relTime': None,
                }
            ],
            'provider': [],
            'sample_type': [],
            'missing_value': [],
        }
    }
}

GET_JSON_RESPONSES = {
    '/v2/tree_nodes?depth=0&tags=True&counts=False': {
        'tree_nodes': [
            {
                'fullName': '\\Dummy'
            }
        ]
    }

}