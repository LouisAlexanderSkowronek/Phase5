import os

from sys import exit

from voc import Voc
from phase import Phase

class Phase5:
    def __init__(self) -> None:
        self.phases = [
            Phase(Phase5.read_vocset('vocs/phase5.csv')),
            Phase(Phase5.read_vocset('vocs/phase4.csv')),
            Phase(Phase5.read_vocset('vocs/phase3.csv')),
            Phase(Phase5.read_vocset('vocs/phase2.csv')),
            Phase(Phase5.read_vocset('vocs/phase1.csv'))
        ]

    
    def run_main_menu(self) -> None:
        idx = Phase5.get_option_number(['Learn', 'Add new vocabularies'])

        if idx == 0:
            self.check_phase_n(5)
        elif idx == 1:
            self.run_menu_add_vocabularies()
        else:
            raise NotImplementedError('You should never see this message. Contact the developer immediately to fix this bug!')

    
    def check_phase_n(self, n: int) -> None:
        correct_vocs = []
        incorrect_vocs = []
        vocs = self.phases[5-n].vocs
        for voc in vocs:
            print(voc.native)
            answer = Phase5.input_or_exit('Greek: ', self.forward_phase_n, n=n, correct_vocs=correct_vocs, incorrect_vocs=incorrect_vocs).strip().lower()
            if answer == voc.greek:
                print('Correct!')
                correct_vocs.append(voc)
            else:
                print('No, it\'s: ' + voc.greek)
                incorrect_vocs.append(voc)

            print('\n')
        
        self.forward_phase_n(n, correct_vocs, incorrect_vocs)
    

    def forward_phase_n(self, n: int, correct_vocs: list[Voc], incorrect_vocs: list[Voc]) -> None:
        if n <= 0:
            raise ValueError('n must be positive!')
        
        if n == 1:
            Phase5.shift_vocs_from_phase_to_phase(incorrect_vocs, 'vocs/phase1.csv', 'vocs/phase5.csv')
            Phase5.shift_vocs_from_phase_to_phase(correct_vocs, 'vocs/phase1.csv', 'vocs/finished.csv')
            print('Finished!')
        else:
            Phase5.shift_vocs_from_phase_to_phase(incorrect_vocs, f'vocs/phase{n}.csv', 'vocs/phase5.csv')
            Phase5.shift_vocs_from_phase_to_phase(correct_vocs, f'vocs/phase{n}.csv', f'vocs/phase{n-1}.csv')
            self.check_phase_n(n-1)
    

    def shift_vocs_from_phase_to_phase(vocs: list[Voc], src_phase_filepath: str, dst_phase_filepath: str) -> None:
        src_vocs_to_filter: list[Voc] = Phase5.read_vocset(src_phase_filepath)

        for voc in vocs:
            src_vocs_to_filter.remove(voc)

        with open(src_phase_filepath, 'w+') as vocfile:
            vocfile.writelines([str(voc)+'\n' for voc in src_vocs_to_filter])
        
        Phase5.append_vocs_to_vocset(vocs, dst_phase_filepath)
    

    def run_menu_add_vocabularies(self) -> None:
        print("You can type 'exit' anytime to quit")
        vocs_to_add = []
        func_to_save_vocs_on_exit = lambda: Phase5.append_vocs_to_vocset(vocs_to_add, 'vocs/phase5.csv')
        while True:
            native = Phase5.input_or_exit('Vocabulary in native language: ', func_to_save_vocs_on_exit).strip().lower()
            greek = Phase5.input_or_exit('Vocabulary in Greek: ', func_to_save_vocs_on_exit).strip().lower()
            print('\n')

            vocs_to_add.append(Voc(native, greek))
        

    def read_vocset(filepath: str) -> list[str]:
        ret = []

        if not os.path.exists(filepath):
            os.system('touch ' + filepath)
            return []

        with open(filepath, 'r') as vocfile:
            for entry in vocfile:
                native, greek = entry.strip().split(',')
                ret.append(Voc(native, greek))
        
        return ret
    

    def append_vocs_to_vocset(vocs: list[Voc], filepath: str) -> None:
        with open(filepath, 'a+') as vocfile:
            vocfile.writelines([str(voc)+'\n' for voc in vocs])
            

    def input_or_exit(msg: str = '', operation_on_exit = lambda: None, **params) -> str:
        inp = input(msg)

        if inp.strip().lower() == 'exit':
            operation_on_exit(**params)
            exit(0)
        
        return inp


    def get_option_number(option_descriptions: list, start_message='Options:', end_message='Enter number of the option you want to select: ', try_again=True, start_at=0) -> int:
        print("You can type 'exit' anytime to quit")
        
        while True:
            print(start_message)
            for i, option_description in enumerate(option_descriptions):
                print(f'[{i+start_at}]: {option_description}')

            try:
                option_number = int(Phase5.input_or_exit(end_message))
                if option_number-start_at < 0 or option_number-start_at >= len(option_descriptions): raise ValueError
                return option_number
            except ValueError:
                print('Invalid value. Try again!')
