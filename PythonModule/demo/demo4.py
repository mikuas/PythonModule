# coding:utf-8


class Test:

    def getName(self):
        return "Test"

    class Test(Test):

        def getName(self):
            return "Test > Test"

        class Test(Test):

            def getName(self):
                return "Test > Test > Test"

            class Test(Test):

                def getName(self):
                    return "Test > Test > Test > Test"

                class Test(Test):

                    def getName(self):
                        return "Test > Test > Test > Test > Test"

                    class Test(Test):

                        def getName(self):
                            return "Test > Test > Test > Test > Test > Test"

                        class Test(Test):

                            def getName(self):
                                return "Test > Test > Test > Test > Test > Test > Test"

                            class Test(Test):

                                def getName(self):
                                    return "Test > Test > Test > Test > Test > Test > Test > Test"

                                class Test(Test):

                                    def getName(self):
                                        return "Test > Test > Test > Test > Test > Test > Test > Test > Test"

                                    class Test(Test):

                                        def getName(self):
                                            return "Test > Test > Test > Test > Test > Test > Test > Test > Test > Test"

                                        class Test(Test):

                                            def getName(self):
                                                return "Test > Test > Test > Test > Test > Test > Test > Test > Test > Test > Test"


if __name__ == '__main__':
    t = Test()
    print(t.getName())