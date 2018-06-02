import text_to_image as tti


tti.encode("My glass shall not persuade me I am old, So long as youth and thou are of one date; But when in thee time's furrows I behold, Then look I death my days should expiate. For all that beauty that doth cover thee Is but the seemly raiment of my heart, Which in thy breast doth live, as thine in me","p.png")

print(tti.decode("p.png"))
