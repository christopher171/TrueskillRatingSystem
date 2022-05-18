#!/usr/bin/env python
# coding: utf-8

# In[ ]:


def SkillToPerformance(message_to_skill, beta = 10): # m->p_i,j
#принимаем на вход m->s_i, j
  return Message(message_to_skill.mu, message_to_skill.sigma2 + beta ** 2)

#потом можно используя эту функцию менять значения в factor_graph для разных индексов вершин (для общего цикла)

#TODO - поправить нижние функции, чтобы они принимали messages, а не Nodes, и возвращали Message( , )

def PerformanceToTeam(performance_messages, alphas): #m->t_j
  return SumMessages(performance_messages, alphas)

def TeamToU(team_massage): #m
  return Message(0, team_massage.sigma2)

def UToTeam(u_message, epsilon): #Node, Node
  return GetIndicatorLower(u_message, epsilon)

def TeamToI(team_massage, u_massage):
  return ProdMessages([team_massage, u_massage])

def TeamToL(team_messages, u_messages): #teams with one place, list of Messages (n), list of Messages (n)
  new_messages = []
  for i in range(len(team_messages)):
    new_messages.append(SumMessages([team_messages[i], AlphaMessage(u_messages[i], -1)], 0))
  return ProdMessages(new_messages)

##testing

def ListTeamsToL(team_messages, u_messages):
  new_messages = []
  for i in range(len(team_messages)):
    new_messages.append(SumMessages([team_messages[i], AlphaMessage(u_messages[i], -1)], 0))
  return new_messages

##testing

def TeamToPerformance(team_message, other_performance_messages, alpha, other_alphas): 
#Node, Node, list of Nodes (n teammates - 1), list of const
  return AlphaMessage(SumMessages([team_message,                                    AlphaMessage(SumMessages(other_performance_messages, other_alphas), -1)]),                                (1 / alpha))

def PerformanceToSkill(performance_message, skill_message, beta = 4.1): #Node, Node
  return ProdMessages([skill_message, Message(performance_message.mu, performance_message.sigma2 + (beta ** 2))])

#фукнции для сообщения нижнего слоя
import copy

def LToIndicatorL(message_to_l): #m lk->dk, l_k+1->dk
  return message_to_l

#функции далее надо выполнять в цикле до сходимости функций с индикаторами

def IndicatorLToDifference(message_to_l_first, message_to_l_second): #m ->dk
  return message_to_l_first - message_to_l_second

def DifferenceToIndicatorL(message_to_difference): #m dk->
  return GetIndicatorGreater(message_to_difference, 2 * our_epsilon)

def IndicatorLToFirstL(message_from_diff, message_from_l_sec_to_d): #m dk->lk
  return message_from_diff + message_from_l_sec_to_d

def IndicatorLToSecondL(message_from_diff, message_from_l_first_to_d): #m dk->l_k+1
  return message_from_l_first_to_d - message_from_diff

def LToIndicatorU(message_prev_diff_to_this_l, this_diff_to_this_l, messages_from_u_to_l, index): #m l_k->u_j
  #print(index, "index in L to indicator U")
  #print(len(messages_from_u_to_l), "len messages from u to l")
  if not message_prev_diff_to_this_l:
    ans = this_diff_to_this_l #первый аргумент может быть пустым
  else:
    ans = message_prev_diff_to_this_l * this_diff_to_this_l
  for mes in messages_from_u_to_l:
    ans *= mes
  ans /= messages_from_u_to_l[index] #T(k) \ j
  return ans

def ToU(message_to_l, message_from_t): #m->uj
  return message_to_l - message_from_t

def FromU(message_to_u, epsilon): #m uj->
  return GetIndicatorLower(message_to_u, epsilon)

def UToL(message_from_u, message_from_t): #m uj->lk
  return message_from_t - message_from_u

def ToL(messages_from_u_to_l): #m lk->

  ans = messages_from_u_to_l[0]
  for i in range(1, len(messages_from_u_to_l)):
    ans *= messages_from_u_to_l[i]
  return ans

def LToD(index, message_from_prev_d_to_l, message_to_l): #m l_k->dk
#важно первая вершина или нет, в зависимости от index может не быть 2 аргумента
  if index == 0:
    return message_to_l
  return message_to_l * message_from_prev_d_to_l

def LToPreviousD(index, message_from_d_to_l, message_to_l, len_d): #m l_k->d_k-1
#последним аргументом передаем d
  if index == 2 * len_d - 1: 
    return message_to_l
  return message_from_d_to_l * message_to_l

