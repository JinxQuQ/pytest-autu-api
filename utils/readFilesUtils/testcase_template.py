#!/usr/bin/python3
# -*- coding: utf-8 -*-
# @Time    : 2022/4/25 20:02
# @Author  : 余少琪
# @Email   : 1603453211@qq.com
# @File    : testcase_template
# @describe: 用例模板

import datetime
import os
from utils.readFilesUtils.yamlControl import GetYamlData
from common.setting import ConfigHandler


def write_testcase_file(allure_epic, allure_feature, class_title,
                        func_title, case_path, yaml_path, file_name, allure_story):
    """

        :param allure_story:
        :param file_name: 文件名称
        :param allure_epic: 项目名称
        :param allure_feature: 模块名称
        :param class_title: 类名称
        :param func_title: 函数名称
        :param case_path: case 路径
        :param yaml_path: yaml 文件路径
        :return:
        """
    author = GetYamlData(ConfigHandler.config_path).get_yaml_data()['TesterName']
    now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    page = f'''#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time   : {now}
# @Author : {author}


import allure
import pytest
from common.setting import ConfigHandler
from utils.readFilesUtils.get_yaml_data_analysis import CaseData
from utils.assertUtils.assertControl import Assert
from utils.requestsUtils.requestControl import RequestControl


TestData = CaseData(ConfigHandler.data_path + r'{yaml_path}').case_process()


@allure.epic("{allure_epic}")
@allure.feature("{allure_feature}")
class Test{class_title}:

    @allure.story("{allure_story}")
    @pytest.mark.parametrize('in_data', TestData, ids=[i['detail'] for i in TestData])
    def test_{func_title}(self, in_data, case_skip):
        """
        :param :
        :return:
        """

        res = RequestControl().http_request(in_data)
        Assert(in_data['assert']).assert_equality(response_data=res['response_data'], 
                                                  sql_data=res['sql_data'])


if __name__ == '__main__':
    pytest.main(['{file_name}', '-s', '-W', 'ignore:Module already imported:pytest.PytestWarning'])
'''
    if not os.path.exists(case_path):
        with open(case_path, 'w', encoding="utf-8") as f:
            f.write(page)
