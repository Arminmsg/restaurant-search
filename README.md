Question 1: Hello,

I'm new to search engines, and there are a lot of concepts I'm not educated on. To make my onboarding smoother, it'd help if you could provide me with some definitions of the following concepts:

Records
Indexing
I'm also struggling with understanding what types of metrics would be useful to include in the "Custom Ranking."

Cheers, George

Answer 1:
Hello George,
A Record is a data entry, if you’re using Algolia for your ecommerce site a single record would be product information. (e.g. size, price, popularity) about a single product. https://www.algolia.com/doc/glossary/#record here is a link to our documentation that is explaining it closer.

An Index consists of multiple records, so it’s a collection of all your records. In the ecommerce use case, you would have multiple products (record) that you want to search and the Index would contain all of these.
https://www.algolia.com/doc/glossary/#index, the documentation for index.

That’s a good question, It depends on your use case and what kind of metrics should be selected. 
For example our ecommerce customers select popularity as their custom ranking value, since these products usually have a higher conversion rate. If you’re providing a search feature to find stores close by, you should consider proximity. 
Can you elaborate a little bit more on your concrete use case and what goals you are trying to achieve with Algolia?

If there are any other questions open, just send me an email. 

Cheers, Armin


Question 2: Hello,

Sorry to give you the kind of feedback that I know you do not want to hear, but I really hate the new dashboard design. Clearing and deleting indexes are now several clicks away. I am needing to use these features while iterating, so this is inconvenient.

Regards, Matt

Answer 2: Hello Matt,
Thanks for the honest feedback, every feedback is appreciated. I’ll report it back to our product manager. I would be interested to learn more about your workflow and understand it better. Do you have time for a call to help me understand what you’re doing and if there is an easier way to achieve your goals?

Are you available tomorrow at 16:30?

Regards, Armin


Question 3: Hi,

I'm looking to integrate Algolia in my website. Will this be a lot of development work for me? What's the high level process look like?

Regards, Leo


Hi Leo,
Can you share more information about your website and the project? What tech are you using, what are your goals?

As the first step you need to create an application and Index on your Algolia Dashboard. You then need to upload your data to the Index. This can be done through the UI (Upload a JSON/CSV), through the REST API or one of our integrations (https://www.algolia.com/developers/integrations/)

After the data is imported you need to integrate it with your frontend. If you’re using one of the out of the box integrations we have guides now to connect it to your platform (Shopify, Wordpress etc). If you’re using the REST API you can use one of our js libraries to make the integrations easier. https://www.algolia.com/doc/guides/building-search-ui/what-is-instantsearch/js/

We also have UI Libraries to make the build process easier https://www.algolia.com/developers/search-ui/ 

This is the basic setup, there are also some additional steps that you can take (e.g. defining customer ranking properties, facets) to make the search experience more customized.

If there are any other questions open, just send me an email. 

Regards, Armin