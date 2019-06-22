import requests
import time
import platform #for hostname
from prometheus_client import start_http_server, Gauge, registry, Counter


class MineratorMetrics():
    def __init__(self):
        #TODO: DDR4 stuff
        #peak values are commented out

        labels = ['rig', 'device']
        self.voltage = Gauge('minerator_voltage', 'Voltage (V)', labels)
        
        #BMC stuff
        self.vin = Gauge('minerator_vin', "Vin (V)", labels)
        #self.vinpeak = Gauge('minerator_vinpeak', "Vin Peak (V)", labels)
        self.vccintphases = Gauge('minerator_vccintphases', "VCCINT Phases", labels)
        self.power_level = Gauge('minerator_power_level', 'Power Level (W)', labels)

        #VCTRL temp is here too, but we handle that below with health labels

        #TODO: find out what these are for
        #self.iinpeak = Gauge('minerator_iin_peak', "Peak IIN", labels)
        self.ichip = Gauge('minerator_ichip', "current ?", labels)
        self.iin = Gauge('minerator_iin', "current ?", labels)
        self.status_input = Gauge('minerator_status_input', 'Status Input', labels)
        self.status_cml = Gauge('minerator_status_cml', 'Status CML', labels)
        
        #BMC->ADC stuff
        self.aux12v = Gauge('minerator_aux12v', 'AUX12V (V)', labels) 
        self.aux12v_hp = Gauge('minerator_aux12v_health', 'AUX12V Health', labels)#inputVoltageAUX
        self.aux12v_current = Gauge('minerator_aux12_current', 'AUX12V Current (A)', labels) 
        self.aux12v_current_hp = Gauge('minerator_aux12_current_health', 'AUX12V Current Health', labels) #inputCurrentAUX

        self.aux3v3 = Gauge('minerator_aux3v3', 'AUX3V3 (V)', labels)
        self.aux3v3_current = Gauge('minerator_aux3v3_current', 'AUX3V3 Current (A)', labels)

        #TODO: missing metric: 'auxTemperature'
        #TODO: missing metric: 'ddr4vppBtm'
        #TODO: missing metric: 'ddr4vppTop'
        #TODO: missing metric: 'dimmTemperature'
        
        self.fan_speed = Gauge('minerator_fan_speed', 'Fan Speed', labels)
        self.fan_temp = Gauge('minerator_fan_temperature', 'Fan Temp (C)', labels)
        self.fpga_temp = Gauge('minerator_fpga_temp', 'FPGA Temp (C)', labels)
        self.input_power = Gauge('minerator_input_power', 'Input Power (W)', labels)
        self.input_power_hp = Gauge('minerator_input_power_health', 'Input Power Health', labels) #inputPower

        #TODO: find out what these are for
        self.mgt0v9avcc = Gauge('minerator_mgt0v9avcc', '??', labels)
        self.mgtavtt = Gauge('minerator_mgtavtt', '??', labels)
        #=----
        self.pex12v = Gauge('minerator_pex12v', 'PEX12V (V)', labels) 
        self.pex12v_hp = Gauge('minerator_pex12v_health', 'PEX12V Health', labels) #inputVoltagePEX
        self.pex12vcurrent = Gauge('minerator_pex12v_current',  'PEX12V Current (A)', labels)
        self.pex12vcurrent_hp = Gauge('minerator_pex12v_current_health',  'PEX12V Current (A)', labels) #inputCurrentPEX

        self.pex3v3 = Gauge('minerator_pex3v3', 'PEX3V3 (V)', labels)
        self.pex3v3current = Gauge('minerator_pex3v3_current',  'PEX3V3 Current (A)', labels)
        self.sw12v = Gauge('minerator_sw12v', 'SW12V (V)', labels)
        self.sys5v5 = Gauge('minerator_sys5v5', 'SYS5V5', labels)
        self.vcc0v85 = Gauge('minerator_vcc0v85', 'VCC0v85 (V)', labels)
        self.vcc1v2top = Gauge('minerator_vcc1v2top', 'VCC1v2 Top (V)', labels)
        self.vcc1v8 = Gauge('minerator_vcc1v8', 'VCC1v8 (V)', labels)

        self.vccint = Gauge('minerator_vccint', 'VCCINT (V)', labels)
        self.vccint_current = Gauge('minerator_vccint_current', 'VCCINT Current (A)', labels) #vccintCurrent
        self.vccint_current_hp = Gauge('minerator_vccint_current_health', 'VCCINT Current Health', labels) #vccintCurrent
        self.vrctrl_temp = Gauge('minerator_vrctrl_temp', 'VRCTRL Temp (C)', labels)
        self.vrctrl_temp_hp = Gauge('minerator_vrctrl_temp_health', 'VRCTRL Temp Health', labels) #vrCtrl


        #Fee
        f_labels = ['rig', 'algo', 'name']
        self.fee_accepted = Gauge('minerator_fee_accepted', 'Fee Accepted (MH)', f_labels)
        self.fee_calculated = Gauge('minerator_fee_calculated', 'Fee Calculated (MH)', f_labels)
        self.fee_found = Gauge('minerator_fee_found', 'Fee Found (MH)', f_labels)
        self.fee_requested = Gauge('minerator_fee_requested', 'Fee Requested (MH)', f_labels)
        self.fee_submitted = Gauge('minerator_fee_submitted', 'Fee Submitted (MH)', f_labels)
        self.fee_valid = Gauge('minerator_fee_valid', 'Fee Valid (MH)', f_labels)

        self.fee_accepted_per_min = Gauge('minerator_fee_accepted_per_min', 'Fee Accepted/minute (MH)', f_labels)
        self.fee_calculated_per_min = Gauge('minerator_fee_calculated_per_min', 'Fee Calculated/minute (MH)', f_labels)
        self.fee_found_per_min = Gauge('minerator_fee_found_per_min', 'Fee Found/minute (MH)', f_labels)
        self.fee_requested_per_min = Gauge('minerator_fee_requested_per_min', 'Fee Requested/minute (MH)', f_labels)
        self.fee_submitted_per_min = Gauge('minerator_fee_submitted_per_min', 'Fee Submitted/minute (MH)', f_labels)
        self.fee_valid_per_min = Gauge('minerator_fee_valid_per_min', 'Fee Valid/minute (MH)', f_labels)


        #Phase
        p_labels = ['rig', 'device', 'phase']
        self.phase_iout = Gauge('minerator_phase_iout', 'Phase IOUT', p_labels)
        self.phase_vout = Gauge('minerator_phase_vout', 'Phase VOUT', p_labels)
        self.phase_temp = Gauge('minerator_phase_temp', 'Phase Temp (C)', p_labels) 
        self.phase_temp_hp = Gauge('minerator_phase_temp_health', 'Phase Temp Health', p_labels)#use bmc.adc.health.vrPower for HP

        #Sysmon
        s_labels = ['rig', 'device', 'sysmon']
        self.sysmon_temp = Gauge('minerator_sysmon_temperature', 'Sysmon Temp (C)', s_labels)
        self.sysmon_vccaux = Gauge('minerator_sysmon_vccaux', 'Sysmon VCCAUX (V)', s_labels)
        self.sysmon_vccbram = Gauge('minerator_sysmon_vccbram', 'Sysmon VCCBRAM (V)', s_labels)
        self.sysmon_vccint = Gauge('minerator_sysmon_vccint', 'Sysmon VCCINT (V)', s_labels)
        self.sysmon_hp = Gauge('minerator_sysmon_health', 'Sysmon Temp Health', s_labels)

        #Core
        c_labels = ['rig', 'device', 'core']
        self.clock_multiplier = Gauge('minerator_core_clock_multiplier', 'Clock Multiplier', c_labels)
        self.clock_multiplier_hp = Gauge('minerator_core_clock_multiplier_health', 'Clock Multiplier Health', c_labels)
        self.total_nonces = Gauge('minerator_core_total_nonces', 'Total Nonces', c_labels)
        self.bad_nonces = Gauge('minerator_core_bad_nonces', 'Bad Nonces', c_labels)
        


        self.core_accepted_per_min = Gauge('minerator_core_hashrate_accepted_per_min', 'Accepted Hashrate/minute (MH)', c_labels)
        self.core_calculated_per_min = Gauge('minerator_core_hashrate_calculated_per_min', 'Calculated Hashrate/minute (MH)', c_labels)
        self.core_found_per_min = Gauge('minerator_core_hashrate_found_per_min', 'Found Hashrate/minute (MH)', c_labels)
        self.core_requested_per_min = Gauge('minerator_core_hashrate_requested_per_min', 'Requested Hashrate/minute (MH)', c_labels)
        self.core_submitted_per_min = Gauge('minerator_core_hashrate_submitted_per_min', 'Submitted Hashrate/minute (MH)', c_labels)
        self.core_valid_per_min = Gauge('minerator_core_hashrate_valid_per_min', 'Valid Hashrate/minute (MH)', c_labels)

        self.core_accepted = Gauge('minerator_core_hashrate_accepted', 'Accepted Hashrate (MH)', c_labels)
        self.core_calculated = Gauge('minerator_core_hashrate_calculated', 'Calculated Hashrate (MH)', c_labels)
        self.core_found = Gauge('minerator_core_hashrate_found', 'Found Hashrate (MH)', c_labels)
        self.core_requested = Gauge('minerator_core_hashrate_requested', 'Requested Hashrate (MH)', c_labels)
        self.core_submitted = Gauge('minerator_core_hashrate_submitted', 'Submitted Hashrate (MH)', c_labels)
        self.core_valid = Gauge('minerator_core_hashrate_valid', 'Valid Hashrate (MH)', c_labels)

        #Worksource
        self.worksources = Gauge('minerator_worksources', "Worksource Info", ['rig', 'algorithm', 'pool'])
        w_labels = ['rig', 'algorithm', 'pool']
        self.accepted_per_min = Gauge('minerator_hashrate_accepted_per_min', 'Accepted Hashrate/minute (MH)', w_labels)
        self.calculated_per_min = Gauge('minerator_hashrate_calculated_per_min', 'Calculated Hashrate/minute (MH)', w_labels)
        self.found_per_min = Gauge('minerator_hashrate_found_per_min', 'Found Hashrate/minute (MH)', w_labels)
        self.requested_per_min = Gauge('minerator_hashrate_requested_per_min', 'Requested Hashrate/minute (MH)', w_labels)
        self.submitted_per_min = Gauge('minerator_hashrate_submitted_per_min', 'Submitted Hashrate/minute (MH)', w_labels)
        self.valid_per_min = Gauge('minerator_hashrate_valid_per_min', 'Valid Hashrate/minute (MH)', w_labels)

        self.accepted = Gauge('minerator_hashrate_accepted', 'Accepted Hashrate (MH)', w_labels)
        self.calculated = Gauge('minerator_hashrate_calculated', 'Calculated Hashrate (MH)', w_labels)
        self.found = Gauge('minerator_hashrate_found', 'Found Hashrate (MH)', w_labels)
        self.requested = Gauge('minerator_hashrate_requested', 'Requested Hashrate (MH)', w_labels)
        self.submitted = Gauge('minerator_hashrate_submitted', 'Submitted Hashrate (MH)', w_labels)
        self.valid = Gauge('minerator_hashrate_valid', 'Valid Hashrate (MH)', w_labels)

class MineratorParser():
    def __init__(self, hostname):
        self.name = hostname #for rig label on metrics

    #TODO Refactor
    def update_metrics(self, metrics, data):
        # Notes on calculating MH values from JSON
        #from the JS on the minerator webpage:
        #per_min need: value/60
        #total values need: value/((endTime-startTime)/1000000000)

        #Dividing by 60 gives some bad results (particular when trying to calc rejected shares (negative %))
        #USe the total method for both minute and total values
        #-- update: using total method gives bad results too.. oh well
        filter_min = lambda v: float(v)/60
        def filter_total(start, end, v):
            return float(v) / ((float(end)-float(start))/1000000000)

        #Loop through fee dict

        #first check minerator is loaded.. should have data['fee']['algo'] set
        if not "algo" in data['fee']['allmine-fee-v1'][0]:
            return

        for _, fee_data_list in data['fee'].items():
            fee_data = fee_data_list[0] #TODO: do we need to loop over this fee list?
            for algo_name, algo_info in fee_data['algo'].items():
                stats = algo_info['stats']
                labs = [self.name, algo_name, stats['name']]

                per_min = stats['minute']
                total = stats['total']

                s = per_min['startTime']
                e = per_min['endTime']

                #Avoid divide by zero when minerator api is starting up
                if (s != 0 and e != 0) and ( s != e ):
                    metrics.fee_accepted_per_min.labels(*labs).set(filter_total(s, e, per_min['accepted']))
                    metrics.fee_calculated_per_min.labels(*labs).set(filter_total(s, e, per_min['calculated']))
                    metrics.fee_found_per_min.labels(*labs).set(filter_total(s, e, per_min['found']))
                    metrics.fee_requested_per_min.labels(*labs).set(filter_total(s, e, per_min['requested']))
                    metrics.fee_submitted_per_min.labels(*labs).set(filter_total(s, e, per_min['submitted']))
                    metrics.fee_valid_per_min.labels(*labs).set(filter_total(s, e, per_min['valid']))

                s = total['startTime']
                e = total['endTime']

                #Avoid divide by zero when minerator api is starting up
                if (s != 0 and e != 0) and (s != e):
                    metrics.fee_accepted.labels(*labs).set(filter_total(s, e, total['accepted']))
                    metrics.fee_calculated.labels(*labs).set(filter_total(s, e, total['calculated']))
                    metrics.fee_found.labels(*labs).set(filter_total(s, e, total['found']))
                    metrics.fee_requested.labels(*labs).set(filter_total(s, e, total['requested']))
                    metrics.fee_submitted.labels(*labs).set(filter_total(s, e, total['submitted']))
                    metrics.fee_valid.labels(*labs).set(filter_total(s, e, total['valid']))


        #Loop through worksources dict
        for algo_name, ws_data in data['worksources'].items():
            #Loop through each pool configured for each worksource
            for pool_stats in ws_data:
                pool_name = pool_stats['stats']['name']

                labs = [self.name, algo_name, pool_name]

                per_min = pool_stats['stats']['minute']
                total = pool_stats['stats']['total']

                s = per_min['startTime']
                e = per_min['endTime']

                #Avoid divide by zero when minerator api is starting up
                if (s != 0 and e != 0) and (s != e):
                    metrics.accepted_per_min.labels(*labs).set(filter_total(s, e, per_min['accepted']))
                    metrics.calculated_per_min.labels(*labs).set(filter_total(s, e, per_min['calculated']))
                    metrics.found_per_min.labels(*labs).set(filter_total(s, e, per_min['found']))
                    metrics.requested_per_min.labels(*labs).set(filter_total(s, e, per_min['requested']))
                    metrics.submitted_per_min.labels(*labs).set(filter_total(s, e, per_min['submitted']))
                    metrics.valid_per_min.labels(*labs).set(filter_total(s, e, per_min['valid']))

                s = total['startTime']
                e = total['endTime']

                #Avoid divide by zero when minerator api is starting up
                if (s != 0 and e != 0) and (s != e):
                    metrics.accepted.labels(*labs).set(filter_total(s, e, total['accepted']))
                    metrics.calculated.labels(*labs).set(filter_total(s, e, total['calculated']))
                    metrics.found.labels(*labs).set(filter_total(s, e, total['found']))
                    metrics.requested.labels(*labs).set(filter_total(s, e, total['requested']))
                    metrics.submitted.labels(*labs).set(filter_total(s, e, total['submitted']))
                    metrics.valid.labels(*labs).set(filter_total(s, e, total['valid']))


        #Loop through devices
        #workers is a dict with 1 key.. the key appears to change depending on rig.. just ignore it
        devices = data['workers'][list(data['workers'].keys())[0]]['devices'] #must be a better way than this
        for dev_i, dev in enumerate(devices):
            #BMC stuff
            bmc = dev['bmc']
            l = [self.name, dev_i]
            metrics.vin.labels(*l).set(bmc['vin'])
            metrics.status_cml.labels(*l).set(bmc['statusCML'])
            metrics.ichip.labels(*l).set(bmc['ichip'])
            metrics.vccintphases.labels(*l).set(bmc['vccintPhases'])
            metrics.iin.labels(*l).set(bmc['iin'])
            metrics.power_level.labels(*l).set(bmc['powerLevel'])
            metrics.status_input.labels(*l).set(bmc['statusInput'])

            health = bmc['health']

            #ADC---
            adc = bmc['adc']

            input_power = adc['inputPower']
            vrctrl_temp = dev['bmc']['temperature']

            hp_map = {'rampUp': 0,
                      'slowIncrease': 1,
                      'hold': 2,
                      'slowDecrease': 3,
                      'critical': 4}

            def get_hp(key):
                return hp_map[health[key]]

                
            metrics.aux12v.labels(*l).set(adc['aux12V'])
            metrics.aux12v_hp.labels(*l).set(get_hp('inputVoltageAUX'))
            metrics.aux12v_current.labels(*l).set(adc['aux12VCurrent'])
            metrics.aux12v_current_hp.labels(*l).set(get_hp('inputCurrentAUX'))

            metrics.aux3v3.labels(*l).set(adc['aux3V3'])
            metrics.fan_speed.labels(*l).set(adc['fanSpeed'])
            metrics.fan_temp.labels(*l).set(adc['fanTemperature'])
            metrics.fpga_temp.labels(*l).set(adc['fpgaTemperature'])

            metrics.input_power.labels(*l).set(adc['inputPower'])
            metrics.input_power_hp.labels(*l).set(get_hp('inputPower'))

            metrics.mgt0v9avcc.labels(*l).set(adc['mgt0V9avcc'])
            metrics.mgtavtt.labels(*l).set(adc['mgtavtt'])

            metrics.pex12v.labels(*l).set(adc['pex12V'])
            metrics.pex12v_hp.labels(*l).set(get_hp('inputVoltagePEX'))

            metrics.pex12vcurrent.labels(*l).set(adc['pex12VCurrent'])
            metrics.pex12vcurrent_hp.labels(*l).set(get_hp('inputCurrentPEX'))

            metrics.pex3v3.labels(*l).set(adc['pex3V3'])
            metrics.pex3v3current.labels(*l).set(adc['pex3V3Current'])
            metrics.sw12v.labels(*l).set(adc['sw12V'])
            metrics.sys5v5.labels(*l).set(adc['sys5V5'])
            metrics.vcc0v85.labels(*l).set(adc['vcc0V85'])
            metrics.vcc1v2top.labels(*l).set(adc['vcc1V2Top'])
            metrics.vcc1v8.labels(*l).set(adc['vcc1V8'])
            metrics.vccint.labels(self.name, dev_i).set(adc['vccint'])

            metrics.vccint_current.labels(*l).set(adc['vccintCurrent'])
            metrics.vccint_current_hp.labels(*l).set(get_hp('vccintCurrent'))


            metrics.vrctrl_temp.labels(*l).set(bmc['temperature'])
            metrics.vrctrl_temp_hp.labels(*l).set(get_hp('vrCtrl'))

            #Phases
            for phase_i, phase in enumerate(dev['bmc']['phases']):
                metrics.phase_iout.labels(self.name, dev_i, phase_i).set(phase['iout'])
                metrics.phase_vout.labels(self.name, dev_i, phase_i).set(phase['vout'])
                metrics.phase_temp.labels(self.name, dev_i, phase_i).set(phase['temperature'])
                metrics.phase_temp_hp.labels(self.name, dev_i, phase_i).set(get_hp('vrPower'))

            #sysmon
            for sysmon_i, sysmon in enumerate(dev['sysmon']):
                hp = hp_map[sysmon['health']]
                metrics.sysmon_temp.labels(self.name, dev_i, sysmon_i).set(sysmon['temperature'])
                metrics.sysmon_vccaux.labels(self.name, dev_i, sysmon_i).set(sysmon['vccaux'])
                metrics.sysmon_vccbram.labels(self.name, dev_i, sysmon_i).set(sysmon['vccbram'])
                metrics.sysmon_vccint.labels(self.name, dev_i, sysmon_i).set(sysmon['vccint'])
                metrics.sysmon_hp.labels(self.name, dev_i, sysmon_i).set(hp)


            #Cores--
            for core_i, core in enumerate(dev['cores']):
                clock_multi = core['clock']['multiplier']
                total_nonces = core['clock']['totalNonces']
                bad_nonces = core['clock']['badNonces']
                hp = hp_map[core['clock']['health']]

                metrics.clock_multiplier.labels(self.name, dev_i, core_i).set(clock_multi)
                metrics.clock_multiplier_hp.labels(self.name, dev_i, core_i).set(hp)
                metrics.total_nonces.labels(self.name, dev_i, core_i).set(total_nonces)
                metrics.bad_nonces.labels(self.name, dev_i, core_i).set(bad_nonces)

                per_min = core['stats']['minute']
                total = core['stats']['total']

                s = per_min['startTime']
                e = per_min['endTime']

                #Avoid divide by zero when minerator api is starting up
                if (s != 0 and e != 0) and (s != e):
                    metrics.core_accepted_per_min.labels(self.name, dev_i, core_i).set(filter_total(s, e, per_min['accepted']))
                    metrics.core_calculated_per_min.labels(self.name, dev_i, core_i).set(filter_total(s, e, per_min['calculated']))
                    metrics.core_found_per_min.labels(self.name, dev_i, core_i).set(filter_total(s, e, per_min['found']))
                    metrics.core_requested_per_min.labels(self.name, dev_i, core_i).set(filter_total(s, e, per_min['requested']))
                    metrics.core_submitted_per_min.labels(self.name, dev_i, core_i).set(filter_total(s, e, per_min['submitted']))
                    metrics.core_valid_per_min.labels(self.name, dev_i, core_i).set(filter_total(s, e, per_min['valid']))

                s = total['startTime']
                e = total['endTime']

                #Avoid divide by zero when minerator api is starting up
                if (s != 0 and e != 0) and (s != e):
                    metrics.core_accepted.labels(self.name, dev_i, core_i).set(filter_total(s, e, total['accepted']))
                    metrics.core_calculated.labels(self.name, dev_i, core_i).set(filter_total(s, e, total['calculated']))
                    metrics.core_found.labels(self.name, dev_i, core_i).set(filter_total(s, e, total['found']))
                    metrics.core_requested.labels(self.name, dev_i, core_i).set(filter_total(s, e, total['requested']))
                    metrics.core_submitted.labels(self.name, dev_i, core_i).set(filter_total(s, e, total['submitted']))
                    metrics.core_valid.labels(self.name, dev_i, core_i).set(filter_total(s, e, total['valid']))
class MetricExporter():
    def __init__(self, url="http://localhost", interval=30, port=9091):
        self.url = "{}/api/status".format(url)
        self.port = port
        self.interval = interval
        self.metrics = MineratorMetrics()

        hostname = platform.node()
        self.parser = MineratorParser(hostname)

    def get_data(self):
        return requests.get(self.url).json()

    def start(self):
        start_http_server(port=self.port)
        
        #Loops forever, updating metrics if api up, zeroing all otherwise
        while True:
            #if we can't get the data set everything to 0
            try:
                r = requests.get(self.url)
            except requests.ConnectionError:
                print("CONNECTION ERROR...")
                #self.zero_metrics()
                time.sleep(self.interval)
                continue

            if r.status_code != 200:
                print("MINERATOR RETURNED STATUS CODE {}".format(r.status_code))
                #self.zero_metrics()
                time.sleep(self.interval)
                continue

            self.parser.update_metrics(self.metrics, r.json())
            time.sleep(self.interval)


if __name__ == "__main__":
    MetricExporter().start()


