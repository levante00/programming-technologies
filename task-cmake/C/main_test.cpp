#include "A/index.h"
#include "lib.h"
#include "gtest/gtest.h"
#include <iostream>
#include <string>

TEST(testing_index, checking_struct_Object) {
  Object item;
  ASSERT_TRUE((sizeof(item.number) == 4 && sizeof(item.str) == 32));
}

TEST(testing_Cgener_lib, checking_return_number) {
  int a = 1;
  EXPECT_TRUE(return_number(a) == 36);

  a = 2;
  EXPECT_TRUE(return_number(a) == 49);

  std::string str = "USER";
  EXPECT_TRUE(is_valid(str) == true);

  str = "NOT_USER";
  EXPECT_TRUE(is_valid(str) == false);
}
