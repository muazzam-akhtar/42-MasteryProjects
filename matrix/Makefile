NAME = matrix

SRCS = main.cpp

OBJS = ${SRCS:.cpp=.o}

CXX = c++ -std=c++11

CXXFLAGS = -Wall -Werror -Wextra

${NAME}:	${OBJS}
		${CXX} ${CXXFLAGS} ${OBJS} -o ${NAME}

all:	${NAME}

bonus:	all

clean:
	@rm -rf ${OBJS}

fclean: clean
	@rm -rf ${NAME}

re: fclean all

# --- Debug target ---
debug: CXXFLAGS += -g -O0
debug: fclean ${NAME}
