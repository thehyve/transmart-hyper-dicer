POST_JSON_RESPONSES = {
    '/auth/realms/test/protocol/openid-connect/token': {
        'access_token': '54604e3b-4d6a-419d-9173-4b1af0530bfb',
        'token_type': 'bearer',
        'expires_in': 42695,
        'scope': 'read write'},
    '/v2/observations': {
        'dimensionDeclarations': [
        {
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
                    'name': 'studyId',
                    'type': 'String'
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
        },
        {
            'name': 'Diagnosis ID',
            'dimensionType': 'subject',
            'sortIndex': 2,
            'valueType': 'String',
            'modifierCode': 'CSR_DIAGNOSIS_MOD'
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
                        '2019-05-05 11:11:11',
                        '2019-07-05 11:11:11',
                        '@'
                    ],
                    'dimensionIndexes': [
                        0,
                        0,
                        1,
                        0,
                        0,
                        None,
                        None,
                        None,
                        0
                    ],
                    'numericValue': 20
                },
                {
                    'inlineDimensions': [
                        '2019-07-22 12:00:00',
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
                    'id': 1,
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
                },
                {
                    'id': 2,
                    'trial': 'CATEGORICAL_VALUES',
                    'inTrialId': '3',
                    'subjectIds': {
                        'SUBJ_ID': 'CV:12'
                    },
                    'birthDate': None,
                    'deathDate': None,
                    'age': 28,
                    'race': 'Caucasian',
                    'maritalStatus': None,
                    'religion': None,
                    'sexCd': 'Female',
                    'sex': 'male'
                }
            ],
            'visit': [
                {
                    'id': 1,
                    'patientId': 1,
                    'activeStatusCd': None,
                    'startDate': '2016-03-29T09:00:00Z',
                    'endDate': '2016-03-29T11:00:00Z',
                    'inoutCd': None,
                    'locationCd': None,
                    'lengthOfStay': None,
                    'encounterIds': {
                        'VISIT_ID': 'EHR:62:1'
                    }
                }
            ],
            'trial visit': [
                {
                    'id': 1,
                    'studyId': 'CATEGORICAL_VALUES',
                    'relTimeLabel': '1',
                    'relTimeUnit': None,
                    'relTime': None,
                }
            ],
            'provider': [],
            'sample_type': [],
            'missing_value': [],
            'Diagnosis ID': [
                'D1'
            ]
        }
    }
}

GET_JSON_RESPONSES = {
    '/v2/tree_nodes?depth=0&tags=True&counts=False&constraints=False': {
        'tree_nodes': [
            {
                'name': 'CATEGORICAL_VALUES',
                'fullName': '\\Public Studies\\CATEGORICAL_VALUES\\',
                'studyId': 'CATEGORICAL_VALUES',
                'type': 'STUDY',
                'visualAttributes': [
                    'FOLDER',
                    'ACTIVE',
                    'STUDY'
                ],
                'constraint': {
                    'type': 'study_name',
                    'studyId': 'CATEGORICAL_VALUES'
                },
                'metadata': {
                    'upload date': '2019-07-31'
                },
                'children': [
                    {
                        'name': 'Demography',
                        'fullName': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\',
                        'studyId': 'CATEGORICAL_VALUES',
                        'type': 'UNKNOWN',
                        'visualAttributes': [
                            'FOLDER',
                            'ACTIVE'
                        ],
                        'children': [
                            {
                                'name': 'Age',
                                'fullName': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Age\\',
                                'studyId': 'CATEGORICAL_VALUES',
                                'conceptCode': 'CV:DEM:AGE',
                                'conceptPath': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Age\\',
                                'type': 'NUMERIC',
                                'visualAttributes': [
                                    'LEAF',
                                    'ACTIVE',
                                    'NUMERICAL'
                                ],
                                'constraint': {
                                    'type': 'and',
                                    'args': [
                                        {
                                            'type': 'concept',
                                            'conceptCode': 'CV:DEM:AGE'
                                        },
                                        {
                                            'type': 'study_name',
                                            'studyId': 'CATEGORICAL_VALUES'
                                        }
                                    ]
                                }
                            },
                            {
                                'name': 'Gender',
                                'fullName': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Gender\\',
                                'studyId': 'CATEGORICAL_VALUES',
                                'type': 'CATEGORICAL',
                                'visualAttributes': [
                                    'FOLDER',
                                    'ACTIVE',
                                    'CATEGORICAL'
                                ],
                                'children': [
                                    {
                                        'name': 'Female',
                                        'fullName': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Gender\\Female\\',
                                        'studyId': 'CATEGORICAL_VALUES',
                                        'conceptCode': 'CV:DEM:SEX:F',
                                        'conceptPath': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Gender\\Female\\',
                                        'type': 'CATEGORICAL_OPTION',
                                        'visualAttributes': [
                                            'LEAF',
                                            'ACTIVE',
                                            'CATEGORICAL_OPTION'
                                        ],
                                        'constraint': {
                                            'type': 'and',
                                            'args': [
                                                {
                                                    'type': 'concept',
                                                    'conceptCode': 'CV:DEM:SEX:F'
                                                },
                                                {
                                                    'type': 'study_name',
                                                    'studyId': 'CATEGORICAL_VALUES'
                                                }
                                            ]
                                        }
                                    },
                                    {
                                        'name': 'Male',
                                        'fullName': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Gender\\Male\\',
                                        'studyId': 'CATEGORICAL_VALUES',
                                        'conceptCode': 'CV:DEM:SEX:M',
                                        'conceptPath': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Gender\\Male\\',
                                        'type': 'CATEGORICAL_OPTION',
                                        'visualAttributes': [
                                            'LEAF',
                                            'ACTIVE',
                                            'CATEGORICAL_OPTION'
                                        ],
                                        'constraint': {
                                            'type': 'and',
                                            'args': [
                                                {
                                                    'type': 'concept',
                                                    'conceptCode': 'CV:DEM:SEX:M'
                                                },
                                                {
                                                    'type': 'study_name',
                                                    'studyId': 'CATEGORICAL_VALUES'
                                                }
                                            ]
                                        }
                                    }
                                ]
                            },
                            {
                                'name': 'Race',
                                'fullName': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Race\\',
                                'studyId': 'CATEGORICAL_VALUES',
                                'conceptCode': 'CV:DEM:RACE',
                                'conceptPath': '\\Public Studies\\CATEGORICAL_VALUES\\Demography\\Race\\',
                                'type': 'CATEGORICAL',
                                'visualAttributes': [
                                    'LEAF',
                                    'ACTIVE',
                                    'CATEGORICAL'
                                ],
                                'constraint': {
                                    'type': 'and',
                                    'args': [
                                        {
                                            'type': 'concept',
                                            'conceptCode': 'CV:DEM:RACE'
                                        },
                                        {
                                            'type': 'study_name',
                                            'studyId': 'CATEGORICAL_VALUES'
                                        }
                                    ]
                                }
                            }
                        ]
                    }
                ]
            }
        ]
    },
    '/v2/dimensions': {
        'dimensions': [
            {
                'name': 'study',
                'dimensionType': 'attribute',
                'sortIndex': None,
                'valueType': 'Object',
                'fields': [{'name': 'name', 'type': 'String'}],
                'inline': False
            },
            {
                'name': 'patient',
                'dimensionType': 'subject',
                'sortIndex': 1,
                'valueType': 'Object',
                'fields': [
                    {'name': 'id', 'type': 'Int'},
                    {'name': 'subjectIds', 'type': 'Object'},
                    {'name': 'age', 'type': 'Int'},
                    {'name': 'sex', 'type': 'String'}
                ],
                'inline': False
            },
            {
                'name': 'concept',
                'dimensionType': 'attribute',
                'sortIndex': None,
                'valueType': 'Object',
                'fields': [
                    {'name': 'conceptPath', 'type': 'String'},
                    {'name': 'conceptCode', 'type': 'String'},
                    {'name': 'name', 'type': 'String'}
                ],
                'inline': False
            },
            {
                'name': 'trial visit',
                'dimensionType': 'attribute',
                'sortIndex': None,
                'valueType': 'Object',
                'fields': [
                    {'name': 'id', 'type': 'Int'},
                    {'name': 'relTimeLabel', 'type': 'String'},
                    {'name': 'relTimeUnit', 'type': 'String'},
                    {'name': 'relTime', 'type': 'Int'}
                ],
                'inline': False
            },
            {
                'name': 'start time',
                'dimensionType': 'attribute',
                'sortIndex': None,
                'valueType': 'Timestamp',
                'inline': True
            },
            {
                'name': 'visit',
                'dimensionType': 'attribute',
                'sortIndex': None,
                'valueType': 'Object',
                'fields': [
                    {'name': 'id', 'type': 'Int'},
                    {'name': 'activeStatusCd', 'type': 'String'},
                    {'name': 'startDate', 'type': 'Timestamp'},
                    {'name': 'endDate', 'type': 'Timestamp'},
                    {'name': 'inoutCd', 'type': 'String'},
                    {'name': 'locationCd', 'type': 'String'},
                    {'name': 'encounterIds', 'type': 'Object'}
                ],
                'inline': False
            },
            {
                'name': 'end time',
                'dimensionType': 'attribute',
                'sortIndex': None,
                'valueType': 'Timestamp',
                'inline': True
            },
            {
                'name': 'Diagnosis ID',
                'modifierCode': 'CSR_DIAGNOSIS_MOD',
                'dimensionType': 'subject',
                'sortIndex': 2,
                'valueType': 'String',
                'inline': False
            },
            {
                'name': 'Biomaterial ID',
                'modifierCode': 'CSR_BIOMATERIAL_MOD',
                'dimensionType': 'subject',
                'sortIndex': 4,
                'valueType': 'String',
                'inline': False
            },
            {
                'name': 'Biosource ID',
                'modifierCode': 'CSR_BIOSOURCE_MOD',
                'dimensionType': 'subject',
                'sortIndex': 3,
                'valueType': 'String',
                'inline': False
            }
        ]
    },
    '/v2/studies': {
        'studies': [
            {
                'id': 1,
                'studyId': 'CATEGORICAL_VALUES',
                'bioExperimentId': None,
                'secureObjectToken': 'PUBLIC',
                'dimensions': [
                    'study',
                    'concept',
                    'patient'
                ],
                'metadata': {
                    'conceptCodeToVariableMetadata': {
                        'gender': {
                            'columns': 14,
                            'decimals': None,
                            'description': 'Gender',
                            'measure': 'NOMINAL',
                            'missingValues': {
                                'lower': None,
                                'upper': None,
                                'values': [
                                    -2
                                ]
                            },
                            'name': 'gender1',
                            'type': 'NUMERIC',
                            'valueLabels': {
                                '1': 'Female',
                                '2': 'Male',
                                '-2': 'Not Specified'
                            },
                            'width': 12
                        },
                        'birthdate': {
                            'columns': 22,
                            'decimals': None,
                            'description': 'Birth Date',
                            'measure': 'SCALE',
                            'missingValues': None,
                            'name': 'birthdate1',
                            'type': 'DATE',
                            'valueLabels': {},
                            'width': 22
                        }
                    }
                }

            }
        ]
    },
    '/v2/pedigree/relation_types': {
        'relationTypes': [
            {
                'id': 1, 'biological': False, 'description': 'Parent', 'label': 'PAR', 'symmetrical': False
            },
            {
                'id': 2, 'biological': False, 'description': 'Spouse', 'label': 'SPO', 'symmetrical': True
            },
            {
                'id': 3, 'biological': False, 'description': 'Sibling', 'label': 'SIB', 'symmetrical': True
            },
            {
                'id': 4, 'biological': True, 'description': 'Monozygotic twin', 'label': 'MZ', 'symmetrical': True
            },
            {
                'id': 5, 'biological': True, 'description': 'Dizygotic twin', 'label': 'DZ', 'symmetrical': True
            },
            {
                'id': 6, 'biological': True, 'description': 'Twin with unknown zygosity', 'label': 'COT', 'symmetrical': True
            },
            {
                'id': 7, 'biological': False, 'description': 'Child', 'label': 'CHI', 'symmetrical': False
            }
        ]
    },
    '/v2/pedigree/relations': {
        'relations': [
            {
                'leftSubjectId': 1,
                'relationTypeLabel': 'SPO',
                'rightSubjectId': 2,
                'biological': False,
                'shareHousehold': False
            }
        ]
    }
}
