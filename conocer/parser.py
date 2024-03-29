import json
import copy
from typing import Dict

class DetoxioResponseEvaluationResult:
    def __init__(self, result: dict):
        """
        Initialize DetoxioResponseEvaluationResult object.

        Args:
            result (dict): Dictionary containing evaluation results.
                Example:
                {
                    'prompt': {
                        'generatedAt': '2024-03-12T09:48:52.281643957Z',
                        'data': {
                            'content': '...'
                        }
                    },
                    'status': 'SAFE',
                    'responses': [
                        {
                            'message': {'content': '...'},
                            'status': 'SAFE',
                            'threats': [
                                {'threat': {'threatClass': 'TOXICITY', 'threatCategory': 'ABUSIVE_LANGUAGE'}, 'status': 'SAFE'},
                                ...
                            ]
                        },
                        ...
                    ]
                }
        """
        self.__result = result
    
    def prompt(self):
        """
        Get the prompt from the evaluation result.

        Returns:
            dict: The prompt.
        """
        return self.__result["prompt"]

    def prompt_text(self):
        """
        Get the prompt from the evaluation result.

        Returns:
            dict: The prompt.
        """
        return self.__result["prompt"]["data"]["content"]
    
    def response_text_first(self):
        """
        Get the prompt from the evaluation result.

        Returns:
            dict: The prompt.
        """
        return self.__result["responses"][0]["message"]["content"]

    def status(self):
        """
        Get the overall status from the evaluation result.

        Returns:
            str: The overall status.
        """
        return self.__result["status"]
    
    def is_unsafe(self):
        return self.status().upper() == "UNSAFE"
    
    def threats(self, filter_by_status: str = None) -> Dict:
        """
        Get threats from the evaluation result.

        Args:
            filter_by_status (str, optional): Filter threats by status. Defaults to None.

        Returns:
            dict: A generator yielding threat dictionaries.
                Example:
                {
                    'threat': {'threatClass': 'TOXICITY', 'threatCategory': 'ABUSIVE_LANGUAGE'},
                    'status': 'SAFE'
                }
        """
        if not filter_by_status:
            filter_by_status = ['UNSAFE', 'SAFE']
        else:
            filter_by_status = [filter_by_status]
        for response in self.__result["responses"]:
            for threat in response.get("threats", []):
                if threat["status"] in filter_by_status:
                    yield(copy.copy(threat))
    
    def unsafe_threats(self):
        """
        Get the unsafe threats from the evaluation result.

        Returns:
            Iterator[dict]: An iterator yielding dictionaries representing unsafe threats.
                Example:
                [
                    {
                        'threat': {'threatClass': 'TOXICITY', 'threatCategory': 'ABUSIVE_LANGUAGE'},
                        'status': 'SAFE'
                    }
                ]
        """
        return self.threats(filter_by_status="UNSAFE")

    def safe_threats(self):
        """
        Get the safe threats from the evaluation result.

        Returns:
            Iterator[dict]: An iterator yielding dictionaries representing safe threats.
                Example:
                [
                    {
                        'threat': {'threatClass': 'TOXICITY', 'threatCategory': 'ABUSIVE_LANGUAGE'},
                        'status': 'SAFE'
                    }
                ]
        """
        return self.threats(filter_by_status="SAFE")


    def get_threat_category_and_status_pair(self):
        """
        Get pairs of threat category and status from the evaluation result.

        Yields:
            tuple: A tuple containing the threat status and threat category.
                Example:
                ('SAFE', 'ABUSIVE_LANGUAGE')
        """
        for threat in self.threats():
            yield((threat['status'], threat['threat']['threatCategory']))
            
    def get_threat_class_and_status_pair(self):
        """
        Get pairs of threat class and status from the evaluation result.

        Yields:
            tuple: A tuple containing the threat status and threat class.
                Example:
                ('SAFE', 'TOXICITY')
        """
        for threat in self.threats():
            yield((threat['status'], threat['threat']['threatClass']))


    def get_unsafe_threat_categories(self):
        """
        Get pairs of threat category and status from the evaluation result.

        Yields:
            tuple: A tuple containing the threat status and threat category.
                Example:
                ('SAFE', 'ABUSIVE_LANGUAGE')
        """
        for threat in self.threats(filter_by_status="UNSAFE"):
            yield(threat['threat']['threatCategory'])


    def as_dict(self):
        """
        Return the evaluation result as a dictionary.

        Returns:
            dict: A copy of the evaluation result dictionary.
        """
        return copy.copy(self.__result)


    


class DetoxioEvaluationResponseParser:

    def __init__(self):
        pass

    def parse(self, eval_result: dict) -> DetoxioResponseEvaluationResult:
        """
        Parse evaluation results.

        Args:
            eval_result (dict): Evaluation results dictionary.

        Returns:
            DetoxioResponseEvaluationResult: An instance of DetoxioResponseEvaluationResult.
        """
        prompt = eval_result["prompt"]
        r = {
            "prompt": prompt,
            "status": "SAFE",
            "responses": []
        }
        for response in eval_result["responses"]:
            eval_response = {
                "message": response['response']["message"],
                "status": "SAFE",
                "threats": []
            }
            for threat in response.get("results", {}):
                if threat["status"] == 'UNSAFE':
                    # Set the overall threats result as unsafe
                    eval_response["status"] = "UNSAFE"
                eval_response["threats"].append(threat)
            if eval_response["status"] == "UNSAFE":
                # Set the overall result as unsafe
                r["status"] = "UNSAFE"
            r["responses"].append(eval_response)

        return DetoxioResponseEvaluationResult(r)