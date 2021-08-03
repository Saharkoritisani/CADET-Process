import unittest

class Test_flow_sheet(unittest.TestCase):

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)

    def create_ssr_flow_sheet(self):
        import CADETProcess
        flow_sheet = CADETProcess.FlowSheet(n_comp=2, name='test')

        feed = CADETProcess.unitOperation.Source(n_comp=2, name='feed')
        eluent = CADETProcess.unitOperation.Source(n_comp=2, name='eluent')
        cstr = CADETProcess.unitOperation.Cstr(n_comp=2, name='cstr')
        column = CADETProcess.unitOperation.LumpedRateModelWithoutPores(n_comp=2, name='column')
        outlet = CADETProcess.unitOperation.Sink(n_comp=2, name='outlet')

        flow_sheet.add_unit(feed)
        flow_sheet.add_unit(eluent)
        flow_sheet.add_unit(cstr)
        flow_sheet.add_unit(column)
        flow_sheet.add_unit(outlet)

        flow_sheet.add_connection(feed, cstr)
        flow_sheet.add_connection(cstr, column)
        flow_sheet.add_connection(eluent, column)
        flow_sheet.add_connection(column, cstr)
        flow_sheet.add_connection(column, outlet)

        flow_sheet.add_eluent_source(eluent)
        flow_sheet.add_feed_source(feed)
        flow_sheet.add_chromatogram_sink(outlet)

        return flow_sheet

    def test_unit_names(self):
        flow_sheet = self.create_ssr_flow_sheet()
        unit_names = ['feed', 'eluent', 'cstr', 'column', 'outlet']

        self.assertEqual(list(flow_sheet.units_dict.keys()), unit_names)


    def test_sources(self):
        flow_sheet = self.create_ssr_flow_sheet()

        self.assertIn(flow_sheet.feed, flow_sheet.sources)
        self.assertIn(flow_sheet.eluent, flow_sheet.sources)
        self.assertIn(flow_sheet.cstr, flow_sheet.sources)


    def test_sinks(self):
        flow_sheet = self.create_ssr_flow_sheet()

        self.assertIn(flow_sheet.cstr, flow_sheet.sinks)
        self.assertIn(flow_sheet.outlet, flow_sheet.sinks)


    def test_connections(self):
        flow_sheet = self.create_ssr_flow_sheet()

        expected_connections = {
                'feed': ['cstr'],
                'eluent': ['column'],
                'cstr': ['column'],
                'column': ['cstr', 'outlet'],
                'outlet': []}

        # self.assertDictEqual(flow_sheet.connections_out, expected_connections)


    def test_ssr_flow_rates(self):
        flow_sheet = self.create_ssr_flow_sheet()

        # Injection
        flow_sheet.feed.flow_rate = 0
        flow_sheet.eluent.flow_rate = 0
        flow_sheet.cstr.flow_rate = 1
        flow_sheet.set_output_state('column', 1)

        expected_flow_rates = {
            'feed': {
                'total': (0, 0, 0, 0),
                'destinations': {
                    'cstr': (0, 0, 0, 0),
                },
            },
            'eluent': {
                'total': (0, 0, 0, 0),
                'destinations': {
                    'column': (0, 0, 0, 0),
                },
            },
            'cstr': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'column': (1.0, 0, 0, 0),
                },
            },            
            'column': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'cstr': (0, 0, 0, 0),
                    'outlet': (1.0, 0, 0, 0),
                },
            },
            'outlet': {
                'total': (1.0, 0, 0, 0),
                },
        }        

        self.assertDictEqual(flow_sheet.flow_rates, expected_flow_rates)

        # Elution and Feed
        flow_sheet.feed.flow_rate = 1
        flow_sheet.eluent.flow_rate = 1
        flow_sheet.cstr.flow_rate = 0
        flow_sheet.set_output_state('column', 1)

        expected_flow_rates = {
            'feed': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'cstr': (1.0, 0, 0, 0),
                },
            },
            'eluent': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'column': (1.0, 0, 0, 0),
                },
            },
            'cstr': {
                'total': (0, 0, 0, 0),
                'destinations': {
                    'column': (0, 0, 0, 0),
                },
            },            
            'column': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'cstr': (0, 0, 0, 0),
                    'outlet': (1.0, 0, 0, 0),
                },
            },
            'outlet': {
                'total': (1.0, 0, 0, 0),
                },
        }        
        
        self.assertDictEqual(flow_sheet.flow_rates, expected_flow_rates)

        # Elution
        flow_sheet.feed.flow_rate = 0
        flow_sheet.eluent.flow_rate = 1
        flow_sheet.cstr.flow_rate = 0
        flow_sheet.set_output_state('column', 1)

        expected_flow_rates = {
            'feed': {
                'total': (0, 0, 0, 0),
                'destinations': {
                    'cstr': (0, 0, 0, 0),
                },
            },
            'eluent': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'column': (1.0, 0, 0, 0),
                },
            },
            'cstr': {
                'total': (0, 0, 0, 0),
                'destinations': {
                    'column': (0, 0, 0, 0),
                },
            },            
            'column': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'cstr': (0, 0, 0, 0),
                    'outlet': (1.0, 0, 0, 0),
                },
            },
            'outlet': {
                'total': (1.0, 0, 0, 0),
                },
        }

        self.assertDictEqual(flow_sheet.flow_rates, expected_flow_rates)

        # Recycle
        flow_sheet.feed.flow_rate = 0
        flow_sheet.eluent.flow_rate = 1
        flow_sheet.cstr.flow_rate = 0
        flow_sheet.set_output_state('column', 0)

        expected_flow_rates = {
            'feed': {
                'total': (0, 0, 0, 0),
                'destinations': {
                    'cstr': (0, 0, 0, 0),
                },
            },
            'eluent': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'column': (1.0, 0, 0, 0),
                },
            },
            'cstr': {
                'total': (0, 0, 0, 0),
                'destinations': {
                    'column': (0, 0, 0, 0),
                },
            },            
            'column': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'cstr': (1.0, 0, 0, 0),
                    'outlet': (0, 0, 0, 0),
                },
            },
            'outlet': {
                'total': (0, 0, 0, 0),
                },
        }

        self.assertDictEqual(flow_sheet.flow_rates, expected_flow_rates)

    def create_clr_flow_sheet(self):
        import CADETProcess
        flow_sheet = CADETProcess.FlowSheet(n_comp=2, name='test')

        feed = CADETProcess.unitOperation.Source(n_comp=2, name='feed')
        column = CADETProcess.unitOperation.LumpedRateModelWithoutPores(n_comp=2, name='column')
        outlet = CADETProcess.unitOperation.Sink(n_comp=2, name='outlet')

        flow_sheet.add_unit(feed)
        flow_sheet.add_unit(column)
        flow_sheet.add_unit(outlet)

        flow_sheet.add_connection(feed, column)
        flow_sheet.add_connection(column, outlet)
        flow_sheet.add_connection(column, column)

        return flow_sheet

    def test_clr_flow_rates(self):
        flow_sheet = self.create_clr_flow_sheet()

        # Injection
        flow_sheet.feed.flow_rate = 1
        flow_sheet.set_output_state('column', 0)

        expected_flow_rates = {
            'feed': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'column': (1.0, 0, 0, 0),
                },
            },
            'column': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'outlet': (1.0, 0, 0, 0),
                    'column': (0, 0, 0, 0),                    
                },
            },
            'outlet': {
                'total': (1.0, 0, 0, 0),
                },
        }

        self.assertDictEqual(flow_sheet.flow_rates, expected_flow_rates)


        # Recycle
        flow_sheet.feed.flow_rate = 0
        flow_sheet.set_output_state('column', [0, 1])

        expected_flow_rates = {
            'feed': {
                'total': (0, 0, 0, 0),
                'destinations': {
                    'column': (0, 0, 0, 0),
                },
            },
            'column': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'outlet': (0, 0, 0, 0),
                    'column': (1.0, 0, 0, 0),                    
                },
            },
            'outlet': {
                'total': (0, 0, 0, 0),
                },
        }

        self.assertDictEqual(flow_sheet.flow_rates, expected_flow_rates)

        # Elution
        flow_sheet.feed.flow_rate = 1
        flow_sheet.set_output_state('column', 0)

        expected_flow_rates = {
            'feed': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'column': (1.0, 0, 0, 0),
                },
            },
            'column': {
                'total': (1.0, 0, 0, 0),
                'destinations': {
                    'outlet': (1.0, 0, 0, 0),
                    'column': (0, 0, 0, 0),                    
                },
            },
            'outlet': {
                'total': (1.0, 0, 0, 0),
                },
        } 

        self.assertDictEqual(flow_sheet.flow_rates, expected_flow_rates)


if __name__ == '__main__':
    unittest.main()