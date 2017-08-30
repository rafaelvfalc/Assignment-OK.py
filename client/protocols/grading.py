"""Implements the GradingProtocol, which runs all specified tests
associated with an assignment.

The GradedTestCase interface should be implemented by TestCases that
are compatible with the GradingProtocol.
"""

from client.protocols.common import models
from client.utils import format
import logging
import os
from shutil import copyfile
import json
import requests


log = logging.getLogger(__name__)

#####################
# Testing Mechanism #
#####################

class GradingProtocol(models.Protocol):
    """A Protocol that runs tests, formats results, and sends results
    to the server.
    """
    def run(self, messages):
        """Run gradeable tests and print results and return analytics.

        RETURNS:
        dict; a mapping of test name -> JSON-serializable object. It is up to
        each test to determine what kind of data it wants to return as
        significant for analytics. However, all tests must include the number
        passed, the number of locked tests and the number of failed tests.
        """
        if self.args.score or self.args.export or self.args.unlock or self.args.restore:
            return
        grade(self.assignment.specified_tests, messages, verbose=self.args.verbose)


def grade(questions, messages, env=None, verbose=True):
    format.print_line('~')
    print('Running tests')
    print()
    passed = 0
    failed = 0
    locked = 0

    analytics = {}
    # Check if analytics info is in messages.
    #if 'analytics' in messages:
    #    started = messages['analytics']['started']
    #else:
    #    started = None

    started = None #Lembrar de tirar

    total_of_failed = 0
    total_of_passed = 0
    total_of_locked = 0

    # The environment in which to run the tests.
    for test in questions:
        # run test if the question is not detected, or question detected and started
        if (started is None
            or test.name not in started
            or started[test.name]):

            log.info('Running tests for {}'.format(test.name))
            results = test.run(env)
            passed += results['passed']
            failed += results['failed']
            locked += results['locked']
            analytics[test.name] = results

            total_of_passed += passed
            total_of_failed += failed
            total_of_locked += locked

            if (not failed and not locked):
                # enviar post da questao pro refazer
                # endpoint, nome da questão, ultima questão incorreta e a ultima solução

                with open('/home/treinamento-16/workspace/Assignment-OK.py/hw02.ok') as data_file:
                    data = json.load(data_file)

                endpoint = data["endpoint"]


                question = test.name


                right_sub_list = os.listdir("/home/treinamento-16/workspace/Assignment-OK.py/submissions/right_submissions")
                count_of_right_subs = len(right_sub_list)

                wrong_sub_list = os.listdir(
                    "/home/treinamento-16/workspace/Assignment-OK.py/submissions/wrong_submissions")
                count_of_wrong_subs = len(wrong_sub_list)

                copyfile("/home/treinamento-16/workspace/Assignment-OK.py/hw02.py",
                         "/home/treinamento-16/workspace/Assignment-OK.py/submissions/right_submissions/right_sub" + str(
                             count_of_right_subs + 1) + ".txt")

                with open("/home/treinamento-16/workspace/Assignment-OK.py/submissions/right_submissions/right_sub" + str(
                        count_of_right_subs + 1)  + ".txt", 'r') as myfile:
                    right_sub = myfile.read()

                correct_code = right_sub

                # Caso não contenha nenhuma submissão incorreta
                try:

                    with open("/home/treinamento-16/workspace/Assignment-OK.py/submissions/wrong_submissions/wrong_sub" + str(
                            count_of_wrong_subs) + ".txt", 'r') as myfile:
                        wrong_sub = myfile.read()

                    incorrect_code = wrong_sub

                except FileNotFoundError:
                    print( "---------------------------------------------------------------------\nYou got it in your first try, congrats!")

                #REFAZER

                refazerObj = {}
                refazerObj["EndPoint"] = endpoint
                refazerObj["Question"] = question
                refazerObj["IncorrectCode"] = incorrect_code
                refazerObj["CorrectCode"] = correct_code

                jsonRefazer = json.dumps(refazerObj)
                headers = {'Content-Type': 'application/json'}
                print(requests.post("http://refazer-online.azurewebsites.net/api/examples", data=jsonRefazer, headers=headers).content)


            else:
                sub_list = os.listdir("/home/treinamento-16/workspace/Assignment-OK.py/submissions/wrong_submissions")
                count_of_subs = len(sub_list)

                with open('/home/treinamento-16/workspace/Assignment-OK.py/hw02.ok') as data_file:
                    data = json.load(data_file)

                endpoint = data["endpoint"]

                question = test.name

                copyfile("/home/treinamento-16/workspace/Assignment-OK.py/hw02.py",
                         "/home/treinamento-16/workspace/Assignment-OK.py/submissions/wrong_submissions/wrong_sub" + str(
                             count_of_subs + 1) + ".txt")

                with open("/home/treinamento-16/workspace/Assignment-OK.py/submissions/wrong_submissions/wrong_sub" + str(
                                count_of_subs + 1) + ".txt", 'r') as myfile:
                    wrong_sub = myfile.read()

                incorrect_code = wrong_sub
                refazerObj = {}
                refazerObj["EndPoint"] = endpoint
                refazerObj["Question"] = question
                refazerObj["Code"] = incorrect_code

                jsonRefazer = json.dumps(refazerObj)
                headers = {'Content-Type': 'application/json'}
                print(requests.post("http://refazer-online.azurewebsites.net/api/submissions/fix", data=jsonRefazer,
                                    headers=headers).content)

        else:
            print('It looks like you haven\'t started {}. Skipping the tests.'.format(test.name))
            print()

        if not verbose and (failed > 0 or locked > 0):
            # Stop at the first failed test
            break



    format.print_progress_bar('Test summary', passed, failed, locked,
                              verbose=verbose)
    print()

    messages['grading'] = analytics

protocol = GradingProtocol
