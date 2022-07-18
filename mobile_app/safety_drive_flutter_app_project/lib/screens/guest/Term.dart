import 'package:flutter/material.dart';
import 'package:flutter_lorem/flutter_lorem.dart';

class TermScreen extends StatefulWidget {
  final Function(int) onChangedStep;


  const TermScreen({
    Key? key,
    required this.onChangedStep,
  }) : super(key: key);

  @override
  State<TermScreen> createState() => _TermScreenState();
}

class _TermScreenState extends State<TermScreen> {
  final ScrollController _scrollController = ScrollController();
  bool _termsReaded = false;

  @override
  void initState() {
    super.initState();
    _scrollController.addListener(() {
      if (_scrollController.offset >=
              _scrollController.position.maxScrollExtent &&
          !_scrollController.position.outOfRange) {
        setState(() => _termsReaded = true);
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    return SafeArea(
      child: Scaffold(
        appBar: AppBar(
          titleSpacing: 0.0,
          elevation: 0,
          title: Text('Terms & Conditions'),
          leading: IconButton(
            onPressed: () => widget.onChangedStep(0),
            icon: const Icon(Icons.arrow_back),
          ),
        ),
        body: Padding(
          padding: const EdgeInsets.symmetric(
            horizontal: 20.0,
            vertical: 15.0,
          ),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Expanded(
                child: SingleChildScrollView(
                  controller: _scrollController,
                  physics: const AlwaysScrollableScrollPhysics(),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    mainAxisAlignment: MainAxisAlignment.start,
                    children: [
                      Text(
                        lorem(paragraphs: 4, words: 450),
                      ),
                    ],
                  ),
                ),
              ),
              const SizedBox(
                height: 10.0,
              ),
              ElevatedButton(
                onPressed: !_termsReaded ? null : () => widget.onChangedStep(2),
                child: Padding(
                  padding: const EdgeInsets.symmetric(
                    vertical: 15.0,
                  ),
                  child: Text(
                    'Accept and Continue'.toUpperCase(),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
